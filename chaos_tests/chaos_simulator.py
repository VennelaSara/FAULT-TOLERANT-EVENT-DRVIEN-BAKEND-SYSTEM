import docker
import random
import time

# Connect to Docker
client = docker.from_env()

# List of critical containers to simulate chaos on
services = [
    "order_service",
    "payment_service",
    "shipping_service",
    "kafka",
    "redis",
    "order_postgres",
    "payment_postgres",
    "shipping_postgres"
]

def random_sleep(min_sec=5, max_sec=15):
    """Sleep for a random duration"""
    duration = random.randint(min_sec, max_sec)
    print(f"Sleeping for {duration} seconds...")
    time.sleep(duration)

def stop_container(container_name):
    try:
        container = client.containers.get(container_name)
        print(f"Stopping container: {container_name}")
        container.stop()
    except docker.errors.NotFound:
        print(f"Container {container_name} not found.")

def start_container(container_name):
    try:
        container = client.containers.get(container_name)
        print(f"Starting container: {container_name}")
        container.start()
    except docker.errors.NotFound:
        print(f"Container {container_name} not found.")

def restart_container(container_name):
    try:
        container = client.containers.get(container_name)
        print(f"Restarting container: {container_name}")
        container.restart()
    except docker.errors.NotFound:
        print(f"Container {container_name} not found.")

def chaos_monkey():
    """Run continuous chaos testing"""
    while True:
        # Choose a random service to kill or restart
        container_name = random.choice(services)
        action = random.choice(["stop", "restart"])

        if action == "stop":
            stop_container(container_name)
            random_sleep(5, 10)
            start_container(container_name)
        elif action == "restart":
            restart_container(container_name)

        # Random delay before next chaos event
        random_sleep(10, 20)

if __name__ == "__main__":
    print("Starting Chaos Simulator for Event-Driven System...")
    try:
        chaos_monkey()
    except KeyboardInterrupt:
        print("Chaos Simulator stopped manually.")
