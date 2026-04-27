import json
import os
from strategies import ConsoleOutputStrategy, KafkaOutputStrategy

class StrategyConfigurator:
    @staticmethod
    def get_strategy(force_strategy="default", config_path="config.json"):
        if force_strategy in ["console", "kafka", "redis"]:
            return StrategyConfigurator._create_strategy(force_strategy)

        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                out_type = config.get("output_type", "console")
                print(f"Loaded config: {out_type}")
                return StrategyConfigurator._create_strategy(out_type)
                
        except (FileNotFoundError, json.JSONDecodeError):
            print("\n==================================================")
            print("WARNING: config.json not found or corrupted!")
            print("1. Run and SAVE choice (create new config)")
            print("2. Run WITHOUT saving (one-time)")
            print("==================================================")
            
            choice = input("Select 1 or 2: ").strip()

            # --- ЦЕЙ БЛОК МИ ОНОВЛЮЄМО ---
            valid_strategies = ["console", "kafka", "redis"]
            while True:
                new_strategy = input(f"Enter strategy ({' / '.join(valid_strategies)}): ").strip().lower()
                if new_strategy in valid_strategies:
                    break
                print(f"❌ Error: '{new_strategy}' is not valid. Try again.")
            # -----------------------------

            if choice == "1":
                new_config = {
                    "output_type": new_strategy,
                    "kafka_broker": "localhost:9092",
                    "kafka_topic": "employee_data_topic"
                }
                with open(config_path, "w") as f:
                    json.dump(new_config, f, indent=4)
                print("New config.json created successfully.")

            return StrategyConfigurator._create_strategy(new_strategy)

    @staticmethod
    def _create_strategy(strategy_type):
        if strategy_type == "kafka":
            return KafkaOutputStrategy("localhost:9092", "employee_data_topic")
        elif strategy_type == "redis":
            return ConsoleOutputStrategy() 
        else:
            return ConsoleOutputStrategy()

def run_lab4_process(selected_strategy="default"):
    from dal import CsvFileReader
    from processor import DataProcessor
    
    reader = CsvFileReader()
    strategy = StrategyConfigurator.get_strategy(selected_strategy)
    
    processor = DataProcessor(reader=reader, strategy=strategy)
    processor.process_and_output("onboarding_data.csv")

if __name__ == "__main__":
    run_lab4_process("default")