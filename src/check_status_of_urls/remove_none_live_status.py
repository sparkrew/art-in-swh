import json
import requests
import time

def check_url_status(url:  str, timeout: int = 10) -> bool:
    """
    Check if a URL is accessible.
    
    Args:
        url: The URL to check
        timeout: Request timeout in seconds
        
    Returns:
        True if URL is accessible (status code 200-399), False otherwise
    """
    try:
        # Add https:// if no protocol specified
        if not url. startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Use HEAD request first (faster), fallback to GET if needed
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        
        # Some servers don't support HEAD, try GET if HEAD fails
        if response.status_code == 405 or response.status_code == 404:
            response = requests.get(url, timeout=timeout, allow_redirects=True)
        
        # Consider 2xx and 3xx status codes as "live"
        return 200 <= response.status_code < 400
        
    except requests.exceptions. RequestException as e:
        print(f"  Error:  {str(e)}")
        return False

def update_live_status(data: list, delay: float = 0.5) -> list:
    """
    Update live status for all entries with None values.
    
    Args:
        data: List of entries to process
        delay:  Delay between requests in seconds
        
    Returns: 
        Updated list of entries
    """
    total = len(data)
    checked = 0
    none_count = 0
    
    for i, entry in enumerate(data, 1):
        origin = entry.get('origin', '')
        metadata = entry.get('metadata', {})
        
        # Only check if live is None/null
        if metadata.get('live') is None:
            print(f"[{i}/{total}] Checking:  {origin}")
            is_live = check_url_status(origin)
            metadata['live'] = is_live
            print(f"  → Status: {is_live}")
            checked += 1
            none_count += 1
            
            print(f"  ✓ Updated 'live' status for:  {origin} to {is_live}")
            print(f"  ({checked} URLs checked so far)")
            print(f"  {none_count} URLs had 'live' = None\n")
            
            
            # Small delay to avoid overwhelming servers
            time.sleep(delay)
        else:
            continue
        
        entry['metadata'] = metadata
    
    print(f"\n✓ Checked {checked} URLs")
    return data

def main():
    """Main function to load, process, and save data."""
    
    # Input and output file paths
    input_file = 'output_results_deduplicated.json'
    output_file = 'output_results_deduplicated_no_none.json'
    
    try:
        # Load data from JSON file
        print(f"Loading data from {input_file}...")
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Loaded {len(data)} entries\n")
        
        # Count entries that need checking
        entries_to_check = sum(1 for entry in data if entry.get('metadata', {}).get('live') is None)
        print(f"Found {entries_to_check} entries with 'live' = None\n")
        
        if entries_to_check == 0:
            print("No entries to update!")
            return
        
        # Estimate time
        estimated_time = entries_to_check * 0.5 / 60  # rough estimate in minutes
        print(f"Estimated time: ~{estimated_time:.1f} minutes\n")
        print("Starting status checks.. .\n")
        
        # Update live status
        updated_data = update_live_status(data, delay=0.5)
        
        # Save updated data
        print(f"\nSaving updated data to {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Successfully saved to {output_file}")
        
        # Print summary
        live_count = sum(1 for entry in updated_data if entry.get('metadata', {}).get('live') is True)
        dead_count = sum(1 for entry in updated_data if entry.get('metadata', {}).get('live') is False)
        none_count = sum(1 for entry in updated_data if entry.get('metadata', {}).get('live') is None)
        
        print(f"\nSummary:")
        print(f"  Live URLs: {live_count}")
        print(f"  Dead URLs:  {dead_count}")
        print(f"  Unchecked: {none_count}")
        
    except FileNotFoundError: 
        print(f"Error:  {input_file} not found!")
        print("Please ensure your JSON file exists in the current directory.")
    except json.JSONDecodeError as e:
        print(f"Error:  Invalid JSON format - {e}")
    except Exception as e: 
        print(f"Unexpected error: {e}")

if __name__ == "__main__": 
    main()