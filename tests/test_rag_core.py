
import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
from src.ugentic.core.rag_core import RAGCore, get_text_splitter

class TestRAGCore(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory and RAG instance for testing."""
        self.test_dir = "tests/rag_test_data"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

        # Create dummy files
        with open(os.path.join(self.test_dir, "doc1.txt"), "w") as f:
            f.write("The sky is blue.")
        with open(os.path.join(self.test_dir, "doc2.md"), "w") as f:
            f.write("The grass is green.")
        with open(os.path.join(self.test_dir, "should_be_ignored.log"), "w") as f:
            f.write("This file should not be loaded.")

        # Mock the embeddings model
        self.mock_embeddings = MagicMock()
        
        # Deterministic embedding based on content
        def mock_embed_documents(texts):
            results = []
            for text in texts:
                if "sky" in text:
                    results.append([0.0, 1.0])
                elif "grass" in text:
                    results.append([1.0, 2.0])
                else:
                    results.append([0.0, 0.0])
            return results

        def mock_embed_query(text):
            if "grass" in text:
                return [1.0, 2.0] # Vector for "The grass is green."
            return [0.0, 1.0] # Default vector

        self.mock_embeddings.embed_documents.side_effect = mock_embed_documents
        self.mock_embeddings.embed_query.side_effect = mock_embed_query

        self.splitter = get_text_splitter()
        self.rag_system = RAGCore(self.mock_embeddings, self.splitter)

    def tearDown(self):
        """Clean up the temporary directory after tests."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_load_documents_from_directory(self):
        """Test that the RAG core loads the correct files from a directory."""
        self.rag_system.load_documents_from_directory(self.test_dir)
        self.assertEqual(len(self.rag_system.vector_store), 2)
        self.mock_embeddings.embed_documents.assert_called()

    def test_retrieve_functionality(self):
        """Test the retrieval functionality after loading documents."""
        self.rag_system.load_documents_from_directory(self.test_dir)
        query = "What color is the grass?"
        retrieved_chunks = self.rag_system.retrieve(query, top_k=1)
        self.assertEqual(len(retrieved_chunks), 1)
        self.mock_embeddings.embed_query.assert_called_once_with(query)
        top_chunk = retrieved_chunks[0]
        self.assertEqual(top_chunk["chunk_text"], "The grass is green.")

if __name__ == '__main__':
    unittest.main()
