from typing import Dict, List

from rich.console import Console
from rich.table import Table

from company_finder.search import search_companies

console = Console()


def display_results(results: Dict[str, List[str]]) -> None:
    """Display the categorized search results in a table."""
    table = Table(title="Company Search Results")
    table.add_column("Category", style="green", no_wrap=True)
    table.add_column("URLs", style="cyan")

    for category, urls in results.items():
        url_list = "\n".join(urls)
        table.add_row(category, url_list)

    console.print(table)


def main() -> None:
    console.print("[bold blue]Company Finder Search Tool[/bold blue]")
    query = input("Enter search query: ").strip()
    console.print(f"[yellow]Searching for companies related:[/yellow] {query}")
    results = search_companies(query)
    display_results(results)

    # Salva i risultati in un file JSON
    save = (
        input("Do you want to save the results to a JSON file? (y/n): ").strip().lower()
    )
    if save == "y":
        import json
        import os

        os.makedirs("results", exist_ok=True)
        with open(f"results/{query.replace(' ', '_')}_results.json", "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        console.print(
            f"[green]Results saved to results/{query.replace(' ', '_')}_results.json[/green]"
        )


if __name__ == "__main__":
    main()
