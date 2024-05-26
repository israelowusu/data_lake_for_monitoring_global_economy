from prefect import task, Flow
from prefect.tasks.shell import ShellTask

# Define the task to run the main.py script
run_main_script = ShellTask(command="python main.py")

# Build the Prefect flow
with Flow("Global Economic Data Pipeline") as flow:
    run_main_script()

# Register the flow with Prefect Cloud or run it locally
if __name__ == "__main__":
    flow.run()  # Uncomment to run the flow locally
    # flow.register(project_name="Global Economic Monitoring")  # Register to Prefect Cloud
