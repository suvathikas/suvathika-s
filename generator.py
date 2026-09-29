import os

from dotenv import load_dotenv

load_dotenv()


DISCLAIMER = (
    "This document is an educational draft, not legal advice. "
    "Legal requirements vary by jurisdiction. Have a qualified "
    "lawyer review it before signing, filing, or relying on it."
)


def generate_template(data) -> str:
    """Create a general-purpose legal document template."""

    document = f"""
# {data.document_type.upper()}

**Jurisdiction:** {data.jurisdiction}

**Effective Date:** {data.effective_date}

**Duration:** {data.duration}


## 1. PARTIES

{data.parties}


## 2. PURPOSE

The parties wish to record their understanding
concerning the matter described in this document.

This draft is based only on the information
provided by the user.


## 3. TERMS AND CONDITIONS

{data.terms}


## 4. RESPONSIBILITIES

Each party should perform the responsibilities
agreed upon in the final reviewed document.

The parties should specify any applicable:

- Deadlines
- Deliverables
- Payment details
- Notice procedures
- Acceptance criteria


## 5. CONFIDENTIALITY

Where applicable, the parties should identify
confidential information and specify how it
may be used, protected, and disclosed.

The parties should add any appropriate
exceptions and obligations after legal review.


## 6. CHANGES TO THIS AGREEMENT

Any changes to this document should be
recorded in writing and accepted by
all relevant parties.


## 7. GOVERNING LAW AND DISPUTES

The parties should obtain jurisdiction-specific
legal advice and insert appropriate governing-law
and dispute-resolution provisions.


## 8. ENTIRE AGREEMENT

The parties should clarify whether this document
replaces or supplements any earlier agreements.

Any required integration provisions should
be added after professional review.


## 9. SIGNATURES

**Party 1**

Name: __________________________

Signature: ______________________

Date: ___________________________


**Party 2**

Name: __________________________

Signature: ______________________

Date: ___________________________


---

REVIEW NOTICE

This is a general-purpose starting template.
It is not a complete or jurisdiction-validated
legal instrument.

Add missing details and obtain qualified
legal review before using this document.
"""

    return document.strip()


def generate_with_ai(data) -> str:
    """Generate a draft using an OpenAI-compatible API."""

    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured.")

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    client_options = {
        "api_key": api_key
    }

    base_url = os.getenv("OPENAI_BASE_URL", "").strip()

    if base_url:
        client_options["base_url"] = base_url

    client = OpenAI(**client_options)

    prompt = f"""
Create a clear first draft of a general legal document.

Important requirements:
- Do not claim that the document is legally valid.
- Do not guarantee enforceability.
- Do not invent facts.
- Use placeholders for missing information.
- Do not present the document as legal advice.
- Use clear headings and organized clauses.
- Include signature placeholders.
- Recommend qualified local legal review.
- Avoid unnecessary sensitive personal information.

Document type:
{data.document_type}

Jurisdiction:
{data.jurisdiction}

Parties:
{data.parties}

Terms and instructions:
{data.terms}

Effective date:
{data.effective_date}

Duration:
{data.duration}

Return only the document draft.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a cautious legal-document "
                    "drafting assistant. You do not provide "
                    "legal advice or certify legal validity."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("The AI returned an empty response.")

    return content.strip()


def generate_document(data):
    """
    Select AI generation when an API key is configured.
    Otherwise, use the built-in template.
    """

    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if api_key:
        document = generate_with_ai(data)
        return document, "llm"

    document = generate_template(data)
    return document, "template"