from llama_index.core.postprocessor import SimilarityPostprocessor

def get_reranker():

    return SimilarityPostprocessor(
        similarity_cutoff=0.70
    )