from prefect import flow, task
import subprocess

@task
def run_main_script():
    # Run the main.py script
    result = subprocess.run(["python3", "main.py"], capture_output=True, text=True)
    
    # Check if the script executed successfully
    if result.returncode != 0:
        raise RuntimeError(f"Main script failed with error:\n{result.stderr}")
    
    # Print the output for logging
    print(result.stdout)

@flow
def main_flow():
    run_main_script()

if __name__ == "__main__":
    main_flow()
