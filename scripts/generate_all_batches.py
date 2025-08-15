#!/usr/bin/env python3
"""Generate all 2,000 encyclopedia pages in manageable batches"""
import json
import subprocess
import time
from pathlib import Path

def create_batch_file(tasks: list, batch_num: int, batch_size: int) -> str:
    """Create a batch task file"""
    start_idx = batch_num * batch_size
    end_idx = min(start_idx + batch_size, len(tasks))
    batch_tasks = tasks[start_idx:end_idx]
    
    batch_file = f"agents/encyclopedia/tasks.batch-{batch_num+1:03d}.json"
    with open(batch_file, "w", encoding="utf-8") as f:
        json.dump(batch_tasks, f, indent=2)
    
    return batch_file

def run_batch(batch_file: str, batch_num: int) -> bool:
    """Run a single batch through the agent"""
    print(f"\n🚀 Starting batch {batch_num+1}...")
    print(f"   File: {batch_file}")
    
    try:
        # Run the agent
        cmd = [
            "python", "agents/encyclopedia/agent.py",
            "--tasks", batch_file,
            "--out", "encyclopedia",
            "--model", "gpt-4o-mini"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)  # 30 min timeout
        
        if result.returncode == 0:
            # Count successful generations
            output_lines = result.stdout.strip().split('\n')
            wrote_lines = [line for line in output_lines if line.startswith('Wrote:')]
            print(f"   ✅ Generated {len(wrote_lines)} pages")
            return True
        else:
            print(f"   ❌ Batch failed with return code {result.returncode}")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"   ⏰ Batch {batch_num+1} timed out after 30 minutes")
        return False
    except Exception as e:
        print(f"   💥 Batch {batch_num+1} failed with exception: {e}")
        return False

def main():
    # Load the complete task list
    tasks_file = "agents/encyclopedia/tasks.complete-2000.json"
    if not Path(tasks_file).exists():
        print(f"❌ Task file not found: {tasks_file}")
        print("Run expand_to_2k.py first to generate the complete task list.")
        return
    
    with open(tasks_file, "r", encoding="utf-8") as f:
        all_tasks = json.load(f)
    
    print(f"📚 Loaded {len(all_tasks)} tasks for generation")
    
    # Configuration
    batch_size = 50  # Generate 50 pages per batch
    total_batches = (len(all_tasks) + batch_size - 1) // batch_size
    
    print(f"🔧 Configuration:")
    print(f"   Batch size: {batch_size} pages")
    print(f"   Total batches: {total_batches}")
    print(f"   Estimated time: {total_batches * 5} minutes (5 min/batch)")
    
    # Track progress
    successful_batches = 0
    failed_batches = []
    total_pages = 0
    
    start_time = time.time()
    
    # Process each batch
    for batch_num in range(total_batches):
        batch_file = create_batch_file(all_tasks, batch_num, batch_size)
        
        # Calculate batch info
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, len(all_tasks))
        batch_count = end_idx - start_idx
        
        print(f"\n📦 Batch {batch_num+1}/{total_batches}")
        print(f"   Tasks {start_idx+1}-{end_idx} ({batch_count} items)")
        
        # Run the batch
        if run_batch(batch_file, batch_num):
            successful_batches += 1
            total_pages += batch_count
        else:
            failed_batches.append(batch_num + 1)
        
        # Progress update
        elapsed = time.time() - start_time
        avg_time = elapsed / (batch_num + 1)
        remaining_batches = total_batches - (batch_num + 1)
        eta = remaining_batches * avg_time
        
        print(f"   Progress: {batch_num+1}/{total_batches} batches ({(batch_num+1)/total_batches*100:.1f}%)")
        print(f"   Generated: ~{total_pages} pages")
        print(f"   Time elapsed: {elapsed/60:.1f} min")
        print(f"   ETA: {eta/60:.1f} min")
        
        # Small delay between batches to avoid rate limits
        if batch_num < total_batches - 1:
            time.sleep(2)
    
    # Final summary
    total_time = time.time() - start_time
    print(f"\n🎉 Generation Complete!")
    print(f"   Total time: {total_time/60:.1f} minutes")
    print(f"   Successful batches: {successful_batches}/{total_batches}")
    print(f"   Estimated pages generated: ~{total_pages}")
    
    if failed_batches:
        print(f"   ⚠️  Failed batches: {failed_batches}")
        print(f"   You can retry failed batches individually")
    else:
        print(f"   🎊 All batches completed successfully!")
    
    # Cleanup batch files
    print(f"\n🧹 Cleaning up batch files...")
    for i in range(total_batches):
        batch_file = f"agents/encyclopedia/tasks.batch-{i+1:03d}.json"
        if Path(batch_file).exists():
            Path(batch_file).unlink()
    print(f"   Removed {total_batches} temporary batch files")

if __name__ == "__main__":
    main()
