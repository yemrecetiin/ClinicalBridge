import json
import time
from core.orchestrator import Orchestrator
from evaluation.metrics import check_triage_accuracy, check_ehr_precision_recall, check_anamnesis_completeness, check_hallucination

class EvalHarness:
    def __init__(self, scenarios_path: str):
        self.scenarios_path = scenarios_path
        self.orchestrator = Orchestrator()

    def run_evaluations(self):
        with open(self.scenarios_path, 'r') as f:
            data = json.load(f)
            
        print("Starting Evaluation Harness...")
        scenarios = data.get("scenarios", [])
        
        results = []
        global_stats = {
            "total": len(scenarios),
            "triage_pass": 0,
            "total_latency": 0,
            "hallucinations": 0
        }

        for s in scenarios:
            print(f"--- Running Scenario: {s['name']} ---")
            
            start_time = time.time()
            ccb = self.orchestrator.process_scenario(s)
            latency = time.time() - start_time
            print(f"CCB Output Generated in {latency:.2f} seconds.")
            
            # Extract triage level from CCB for evaluation
            predicted = "Unknown"
            for level in ["Critical", "Urgent", "Routine", "Informational"]:
                if f"**Triage Level:** {level}" in ccb:
                    predicted = level
                    break
                    
            expected = s.get("expected_triage_level")
            accuracy = check_triage_accuracy(predicted, expected)
            hallucinated = check_hallucination(ccb, s["patient_id"])
            ehr_precision, ehr_recall = check_ehr_precision_recall(ccb, ["Hypertension", "Diabetes", "CHF", "Asthma", "A-Fib"])
            anam_completeness = check_anamnesis_completeness(ccb)

            if accuracy:
                global_stats["triage_pass"] += 1
            if hallucinated:
                global_stats["hallucinations"] += 1
            global_stats["total_latency"] += latency

            print(f"Triage Match: {'PASS' if accuracy else 'FAIL'} (Expected: {expected}, Got: {predicted})")
            print(f"EHR Precision: {ehr_precision}% | EHR Recall: {ehr_recall}%")
            print(f"Anamnesis Completeness: {anam_completeness}%")
            print(f"Hallucination Detected: {hallucinated}\n")
            
            # Print the brief snippet
            print(ccb[:300] + "...\n")
            
            results.append({
                "scenario_name": s["name"],
                "passed": accuracy,
                "ccb": ccb
            })

        print("\n=== FINAL SYSTEM METRICS ===")
        print(f"Total Scenarios Run: {global_stats['total']}")
        print(f"Triage Accuracy: {(global_stats['triage_pass']/global_stats['total'])*100:.1f}%")
        print(f"Average Latency: {(global_stats['total_latency']/global_stats['total']):.2f} seconds")
        print(f"Overall Hallucination Rate: {(global_stats['hallucinations']/global_stats['total'])*100:.1f}%\n")
        
        return results
