import flwr as fl

class HospitalClient(
    fl.client.NumPyClient
):

    def get_parameters(
        self,
        config
    ):
        return []

    def fit(
        self,
        parameters,
        config
    ):

        print(
            "Local training happening..."
        )

        return [], 100, {}

    def evaluate(
        self,
        parameters,
        config
    ):

        return 0.1, 100, {
            "accuracy": 0.95
        }

client = HospitalClient()

fl.client.start_numpy_client(
    server_address="localhost:8080",
    client=client
)