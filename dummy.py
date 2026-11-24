from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(url="http://localhost:6333", timeout=10)

client.delete_collection("test_collection")

print(client.collection_exists("test_collection"))

try:
    if not client.collection_exists("test_collection"):
        client.create_collection(collection_name="test_collection", 
                                 vectors_config=VectorParams(size=4, distance=Distance.COSINE))

    test_vec = [[0.1,0.1,0.2,0.2], [0.4,0.4,0.4,0.4], [0.01, 0.002, 0.001, 0.0001], [0.6, 0.7, 0.6, 0.8]]
    client.upsert(
        collection_name = "test_collection",
        wait=True,
        points=[PointStruct(id=i, vector=test_vec[i]) for i in range(len(test_vec))]
    )
except Exception as e:
    print("error occ:", e)


if client.collection_exists("test_collection"):
    info = client.get_collection("test_collection")
    print("True ", info.points_count)
else:
    print("False")


try:
    search_vec = [0.2, 0.2, 0.1, 0.1]
    result = client.query_points(
        collection_name="test_collection",
        query=search_vec,
        with_vectors=True,
        limit=4
    )
    for r in result:
        print(r, "\n")
except Exception as e:
    print("error in search: ", e)

