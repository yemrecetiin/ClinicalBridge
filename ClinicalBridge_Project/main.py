import os
from core.vector_service import VectorService
from evaluation.eval_harness import EvalHarness

def main():
    print("Initializing ClinicalBridge System...")
    
    # 1. Initialize Vector Store (FAISS)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    patient_data_path = os.path.join(base_dir, "data", "patient_cohort.json")
    
    vs = VectorService()
    vs.init_vector_store(patient_data_path)
    
    # 2. Run Evaluations
    scenarios_path = os.path.join(base_dir, "data", "scenarios.json")
    harness = EvalHarness(scenarios_path)
    
    print("\nStarting Evaluation Harness...")
    results = harness.run_evaluations()
    
    print("\n=== FINAL TEST RESULTS ===")
    for r in results:
        status = "✅ PASS" if r['passed'] else "❌ FAIL"
        print(f"{status} - {r['scenario_name']}")

if __name__ == "__main__":
    main()
