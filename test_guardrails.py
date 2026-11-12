import unittest

from langchain_core.runnables import RunnableLambda

from guardrails import (
    MAX_QUESTION_LENGTH,
    NO_SOURCES_FOUND,
    SENSITIVE_INPUT_MESSAGE,
    SENSITIVE_RESPONSE_MESSAGE,
    UNSAFE_REQUEST_MESSAGE,
    UNSAFE_RESPONSE_MESSAGE,
    contains_sensitive_data,
    is_request_allowed,
    validate_question,
    validate_response,
)


class GuardrailsTests(unittest.TestCase):
    def test_validate_question_rejects_empty_and_oversized_input(self):
        self.assertIsNotNone(validate_question("   "))
        self.assertIsNotNone(validate_question("x" * (MAX_QUESTION_LENGTH + 1)))
        self.assertIsNone(validate_question("Summarize the report."))

    def test_sensitive_data_detection_catches_credentials_and_identifiers(self):
        self.assertTrue(contains_sensitive_data("api_key=abcdefgh123456"))
        self.assertTrue(contains_sensitive_data("SSN 123-45-6789"))
        self.assertTrue(contains_sensitive_data("Card 4111 1111 1111 1111"))
        self.assertFalse(contains_sensitive_data("The report was published in 2024."))

    def test_sensitive_question_is_rejected_before_model_use(self):
        self.assertEqual(
            validate_question("My password: mysecretvalue"),
            SENSITIVE_INPUT_MESSAGE,
        )

    def test_request_classifier_fails_closed_on_non_allow_verdict(self):
        allow_llm = RunnableLambda(lambda _: "ALLOW")
        block_llm = RunnableLambda(lambda _: "BLOCK")

        self.assertTrue(is_request_allowed(allow_llm, "Summarize this document."))
        self.assertFalse(is_request_allowed(block_llm, "Unsafe request"))

    def test_response_validation_blocks_sensitive_or_unsafe_content(self):
        allow_llm = RunnableLambda(lambda _: "ALLOW")
        block_llm = RunnableLambda(lambda _: "BLOCK")

        self.assertEqual(
            validate_response(allow_llm, "The password: mysecretvalue"),
            SENSITIVE_RESPONSE_MESSAGE,
        )
        self.assertEqual(
            validate_response(block_llm, "Unsafe content"),
            UNSAFE_RESPONSE_MESSAGE,
        )
        self.assertEqual(
            validate_response(allow_llm, "A safe, useful answer."),
            "A safe, useful answer.",
        )

    def test_sensitive_question_is_rejected_before_rag_processing(self):
        from rag_chain import answer_question

        class NeverCalled:
            def __getattr__(self, _name):
                raise AssertionError("RAG processing should not run")

        answer, sources = answer_question(
            vectorstore=NeverCalled(),
            llm=NeverCalled(),
            memory=NeverCalled(),
            question="My password: mysecretvalue",
        )

        self.assertEqual(answer, SENSITIVE_INPUT_MESSAGE)
        self.assertEqual(sources, NO_SOURCES_FOUND)

    def test_unsafe_request_is_refused_before_rag_processing(self):
        from rag_chain import answer_question

        class NeverCalled:
            def __getattr__(self, _name):
                raise AssertionError("RAG processing should not run")

        answer, sources = answer_question(
            vectorstore=NeverCalled(),
            llm=RunnableLambda(lambda _: "BLOCK"),
            memory=NeverCalled(),
            question="Unsafe request",
        )

        self.assertEqual(answer, UNSAFE_REQUEST_MESSAGE)
        self.assertEqual(sources, NO_SOURCES_FOUND)


if __name__ == "__main__":
    unittest.main()
