import json
import os
import re
from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from woosh.backend.search import search_companies
from woosh.backend.vies import VATInfo, validate_vat

console = Console()


class CompanyData(BaseModel):
    """Company data: VAT + URLs."""

    vat: VATInfo
    urls: Dict[str, List[str]]
    timestamp: datetime = Field(default_factory=datetime.now)


def is_vat_number(text: str) -> bool:
    """Check if text looks like a VAT number."""
    text = text.strip().upper().replace(" ", "")
    # VAT: country code (2 letters) + digits, or just digits (11 for IT)
    return bool(re.match(r"^([A-Z]{2})?\d{8,12}$", text))


def display_vat_data(data: CompanyData) -> None:
    """Display VAT data."""
    vat = data.vat
    vat_full = f"{vat.country_code}{vat.vat_number}"
    status = "[green]✓ Valid[/green]" if vat.is_valid else "[red]✗ Invalid[/red]"

    info = f"""[bold]VAT:[/bold] {vat_full}
[bold]Status:[/bold] {status}
[bold]Company:[/bold] {vat.company_name or 'N/A'}
[bold]Address:[/bold] {vat.company_address or 'N/A'}"""

    console.print(Panel(info, title="VAT Info", border_style="blue"))

    # Show URLs
    table = Table(title="URLs Found")
    table.add_column("Category", style="cyan")
    table.add_column("URLs", style="white")

    for category, urls in data.urls.items():
        if urls:
            table.add_row(category.capitalize(), "\n".join(urls))

    console.print(table)


def display_search_results(results: Dict[str, List[str]]) -> None:
    """Display search results."""
    table = Table(title="Search Results")
    table.add_column("Category", style="green", no_wrap=True)
    table.add_column("URLs", style="cyan")

    for category, urls in results.items():
        if urls:
            url_list = "\n".join(urls[:5])
            if len(urls) > 5:
                url_list += f"\n... and {len(urls) - 5} more"
            table.add_row(category, url_list)

    console.print(table)


def main() -> None:
    console.print(
        Panel.fit(
            "[bold blue]Company Finder[/bold blue]\n"
            "Enter company name or VAT number",
            border_style="blue",
        )
    )

    query = console.input("\n[yellow]Search:[/yellow] ").strip()

    if not query:
        console.print("[red]No input provided[/red]")
        return

    # Smart detection: VAT or name?
    if is_vat_number(query):
        # VAT lookup
        console.print("[cyan]Validating VAT...[/cyan]")
        with console.status("[green]Searching..."):
            vat_info = validate_vat(query)
            if vat_info.is_valid and vat_info.company_name:
                search_query = vat_info.company_name
            else:
                search_query = query
            urls = search_companies(search_query)
            data = CompanyData(vat=vat_info, urls=urls)

        display_vat_data(data)

        # Save option
        if console.input("\n[yellow]Save?[/yellow] (y/n): ").lower() == "y":
            os.makedirs("results", exist_ok=True)
            vat_id = f"{data.vat.country_code}{data.vat.vat_number}"
            filename = f"results/{vat_id}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(
                    data.model_dump(), f, indent=2, ensure_ascii=False, default=str
                )
            console.print(f"[green]Saved to {filename}[/green]")

    else:
        # Company name search
        console.print(f"[cyan]Searching for: {query}[/cyan]")
        with console.status("[green]Searching..."):
            results = search_companies(query)

        display_search_results(results)

        # Save option
        if console.input("\n[yellow]Save results?[/yellow] (y/n): ").lower() == "y":
            os.makedirs("results", exist_ok=True)
            filename = f"results/{query.replace(' ', '_')}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            console.print(f"[green]Saved to {filename}[/green]")


if __name__ == "__main__":
    main()
