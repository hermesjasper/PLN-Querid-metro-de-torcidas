"""Run LLM annotation for prepared reaction prompts.

This script calls an LLM provider only when executed without `--dry-run`.
It reads prompts from `data/llm_inputs/reaction_annotation_prompts.jsonl`
and appends model outputs to `data/llm_outputs/reaction_annotation_predictions.jsonl`.

Supported providers:
- deepseek: OpenAI-compatible Chat Completions API.
- openai: OpenAI Responses API.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "llm_inputs" / "reaction_annotation_prompts.jsonl"
DEFAULT_OUTPUT = (
    PROJECT_ROOT / "data" / "llm_outputs" / "reaction_annotation_predictions.jsonl"
)
DEFAULT_PROVIDER = "deepseek"
DEFAULT_DEEPSEEK_MODEL = "deepseek-v4-flash"
DEFAULT_OPENAI_MODEL = "gpt-5.5"

RESPONSE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "relevancia": {
            "type": "string",
            "enum": ["RELEVANTE", "POUCO_INFORMATIVO", "NAO_RELEVANTE"],
        },
        "tema": {
            "type": "string",
            "enum": [
                "ELENCO",
                "TECNICO",
                "DIRETORIA",
                "ARBITRAGEM",
                "CONTRATACAO",
                "DESEMPENHO_EM_CAMPO",
                "TORCIDA",
                "RIVALIDADE",
                "PATROCINIO",
                "PARCERIA_COMERCIAL",
                "MARKETING",
                "PRODUTO_OFICIAL",
                "CATEGORIA_BASE",
                "FUTEBOL_FEMININO",
                "INGRESSOS",
                "SOCIO_TORCEDOR",
                "COMUNICACAO_DO_CLUBE",
                "OUTRO",
            ],
        },
        "emocao": {
            "type": "string",
            "enum": [
                "ALEGRIA",
                "ORGULHO",
                "RAIVA",
                "FRUSTRACAO",
                "IRONIA",
                "ESPERANCA",
                "ANSIEDADE",
                "DESCONFIANCA",
                "APOIO",
                "NEUTRO",
            ],
        },
        "polaridade": {
            "type": "string",
            "enum": ["POSITIVO", "NEGATIVO", "NEUTRO", "MISTO"],
        },
        "intencao": {
            "type": "string",
            "enum": [
                "ELOGIO",
                "CRITICA",
                "COBRANCA",
                "PROVOCACAO",
                "MEME_PIADA",
                "PERGUNTA",
                "PEDIDO",
                "APOIO",
                "INFORMACAO",
                "OUTRO",
            ],
        },
        "confianca_modelo": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
        },
        "justificativa_curta": {
            "type": "string",
        },
    },
    "required": [
        "relevancia",
        "tema",
        "emocao",
        "polaridade",
        "intencao",
        "confianca_modelo",
        "justificativa_curta",
    ],
}

ALLOWED_VALUES = {
    "relevancia": set(RESPONSE_SCHEMA["properties"]["relevancia"]["enum"]),
    "tema": set(RESPONSE_SCHEMA["properties"]["tema"]["enum"]),
    "emocao": set(RESPONSE_SCHEMA["properties"]["emocao"]["enum"]),
    "polaridade": set(RESPONSE_SCHEMA["properties"]["polaridade"]["enum"]),
    "intencao": set(RESPONSE_SCHEMA["properties"]["intencao"]["enum"]),
}

REQUIRED_LABEL_COLUMNS = list(ALLOWED_VALUES)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Executa anotacao LLM das reacoes preparadas."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--provider",
        choices=["deepseek", "openai"],
        default=os.getenv("LLM_PROVIDER", DEFAULT_PROVIDER),
        help="Provedor LLM a usar. Tambem pode ser definido por LLM_PROVIDER.",
    )
    parser.add_argument(
        "--model",
        default=None,
        help=(
            "Modelo a usar. Se omitido, usa DEEPSEEK_MODEL, OPENAI_MODEL "
            "ou o padrao do provedor."
        ),
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=3,
        help="Quantidade maxima de prompts a processar nesta execucao.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra o que seria processado sem chamar a API.",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=1,
        help="Tentativas extras quando o modelo retorna rotulos invalidos.",
    )
    return parser.parse_args()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            stripped = line.strip()
            if stripped:
                records.append(json.loads(stripped))
    return records


def append_jsonl(record: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_completed_reaction_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    completed: set[str] = set()
    for record in read_jsonl(path):
        reaction_id = record.get("reaction_id")
        if isinstance(reaction_id, str) and reaction_id:
            completed.add(reaction_id)
            continue
        custom_id = record.get("custom_id")
        if isinstance(custom_id, str) and custom_id.startswith("reaction-"):
            completed.add(custom_id.removeprefix("reaction-"))
    return completed


def get_output_text(response: Any) -> str:
    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str) and output_text.strip():
        return output_text

    response_dict = response.model_dump() if hasattr(response, "model_dump") else {}
    output = response_dict.get("output", [])
    for item in output:
        for content in item.get("content", []):
            text = content.get("text")
            if isinstance(text, str) and text.strip():
                return text
    raise RuntimeError("Nao foi possivel extrair texto da resposta do modelo.")


def parse_model_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`").removeprefix("json").strip()
    return json.loads(cleaned)


def find_invalid_labels(labels: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for column in REQUIRED_LABEL_COLUMNS:
        value = str(labels.get(column, "")).strip()
        if value not in ALLOWED_VALUES[column]:
            allowed = ", ".join(sorted(ALLOWED_VALUES[column]))
            errors.append(f"{column}={value or '<vazio>'}; permitidos: {allowed}")
    confidence = labels.get("confianca_modelo")
    if not isinstance(confidence, int | float) or not 0 <= float(confidence) <= 1:
        errors.append("confianca_modelo deve ser numero entre 0 e 1")
    if not str(labels.get("justificativa_curta", "")).strip():
        errors.append("justificativa_curta esta vazia")
    return errors


def build_retry_messages(
    messages: list[dict[str, str]],
    labels: dict[str, Any],
    errors: list[str],
) -> list[dict[str, str]]:
    correction_prompt = {
        "role": "user",
        "content": (
            "A resposta anterior tem rotulos fora da taxonomia. "
            "Corrija usando somente os valores permitidos e devolva apenas JSON valido.\n\n"
            f"Erros encontrados:\n- " + "\n- ".join(errors) + "\n\n"
            "Resposta anterior:\n"
            f"{json.dumps(labels, ensure_ascii=False)}"
        ),
    }
    return [*messages, correction_prompt]


def get_default_model(provider: str) -> str:
    if provider == "deepseek":
        return os.getenv("DEEPSEEK_MODEL", DEFAULT_DEEPSEEK_MODEL)
    return os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL)


def get_chat_output_text(response: Any) -> str:
    choices = getattr(response, "choices", [])
    if not choices:
        raise RuntimeError("A resposta do modelo nao trouxe choices.")

    choice = choices[0]
    message = choice.message
    content = getattr(message, "content", None)
    if isinstance(content, str) and content.strip():
        return content

    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text") or item.get("content")
                if isinstance(text, str):
                    parts.append(text)
        joined = "\n".join(part for part in parts if part.strip())
        if joined.strip():
            return joined

    finish_reason = getattr(choice, "finish_reason", "")
    response_dump = response.model_dump() if hasattr(response, "model_dump") else {}
    raise RuntimeError(
        "Nao foi possivel extrair texto da resposta do modelo. "
        f"finish_reason={finish_reason}; resposta={json.dumps(response_dump, ensure_ascii=False)[:1000]}"
    )


def create_response(
    client: Any,
    *,
    provider: str,
    model: str,
    messages: list[dict[str, str]],
) -> dict[str, Any]:
    if provider == "deepseek":
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            response_format={"type": "json_object"},
            max_tokens=600,
            stream=False,
            extra_body={"thinking": {"type": "disabled"}},
        )
        return parse_model_json(get_chat_output_text(response))

    response = client.responses.create(
        model=model,
        input=messages,
        text={
            "format": {
                "type": "json_schema",
                "name": "reaction_annotation",
                "schema": RESPONSE_SCHEMA,
                "strict": True,
            }
        },
    )
    return parse_model_json(get_output_text(response))


def create_validated_response(
    client: Any,
    *,
    provider: str,
    model: str,
    messages: list[dict[str, str]],
    max_retries: int,
) -> tuple[dict[str, Any], list[str]]:
    current_messages = messages
    last_labels: dict[str, Any] = {}
    last_errors: list[str] = []
    for attempt in range(max_retries + 1):
        labels = create_response(
            client,
            provider=provider,
            model=model,
            messages=current_messages,
        )
        errors = find_invalid_labels(labels)
        if not errors:
            return labels, []

        last_labels = labels
        last_errors = errors
        if attempt < max_retries:
            current_messages = build_retry_messages(messages, labels, errors)

    return last_labels, last_errors


def main() -> None:
    load_dotenv()
    args = parse_args()
    model = args.model or get_default_model(args.provider)
    prompts = read_jsonl(args.input)
    completed = load_completed_reaction_ids(args.output)
    pending = [
        prompt
        for prompt in prompts
        if str(prompt.get("reaction_id", "")) not in completed
    ]
    selected = pending[: args.limit] if args.limit > 0 else pending

    print(f"Provedor: {args.provider}")
    print(f"Modelo: {model}")
    print(f"Prompts totais: {len(prompts)}")
    print(f"Ja processados: {len(completed)}")
    print(f"Selecionados agora: {len(selected)}")

    if args.dry_run:
        for prompt in selected:
            print(f"- {prompt['custom_id']}")
        return

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise SystemExit(
            "Pacote `openai` nao instalado. Rode: "
            ".\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt"
        ) from exc

    if args.provider == "deepseek":
        if not os.getenv("DEEPSEEK_API_KEY"):
            raise SystemExit("Defina DEEPSEEK_API_KEY no arquivo .env antes de executar.")
        client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com",
        )
    else:
        if not os.getenv("OPENAI_API_KEY"):
            raise SystemExit("Defina OPENAI_API_KEY no arquivo .env antes de executar.")
        client = OpenAI()

    for prompt in selected:
        labels, validation_errors = create_validated_response(
            client,
            provider=args.provider,
            model=model,
            messages=prompt["messages"],
            max_retries=args.max_retries,
        )
        output_record = {
            "custom_id": prompt["custom_id"],
            "reaction_id": prompt["reaction_id"],
            **labels,
        }
        if validation_errors:
            output_record["validation_errors"] = validation_errors
        append_jsonl(output_record, args.output)
        status = "ok" if not validation_errors else "ok_com_alerta"
        print(f"{status}: {prompt['custom_id']}")

    print(f"Saida: {args.output}")


if __name__ == "__main__":
    main()
