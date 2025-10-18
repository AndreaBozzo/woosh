"use client";

import { useState } from "react";

interface SearchResults {
  results: Record<string, string[]>;
  total: number;
}

export default function Home() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<SearchResults | null>(null);
  const [error, setError] = useState("");

  async function handleSearch() {
    if (!query.trim()) {
      setError("Inserisci il nome di un'azienda");
      return;
    }

    setLoading(true);
    setError("");
    setResults(null);

    try {
      const res = await fetch(`/api/search?query=${encodeURIComponent(query)}&max_results=100`);

      if (!res.ok) {
        throw new Error("Errore durante la ricerca");
      }

      const data = await res.json();
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Errore durante la ricerca");
    } finally {
      setLoading(false);
    }
  }

  const parseUrl = (url: string) => {
    try {
      const parsed = new URL(url);
      const domain = parsed.hostname.replace("www.", "");
      const path = parsed.pathname + parsed.search;
      return { domain, path: path !== "/" ? path : "" };
    } catch {
      return { domain: url, path: "" };
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-3xl mx-auto px-4 py-16">
        {/* Header - Super minimale */}
        <div className="mb-16">
          <h1 className="text-5xl font-light tracking-tight mb-3">woosh</h1>
          <p className="text-gray-500 text-sm">ricerca aziende</p>
        </div>

        {/* Search - Un solo input, niente pulsante */}
        <div className="mb-12">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSearch()}
            placeholder="nome azienda"
            className="w-full px-0 py-4 text-2xl border-0 border-b-2 border-gray-200 focus:border-black focus:outline-none transition-colors placeholder:text-gray-300"
            autoFocus
          />
          {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
        </div>

        {/* Loading - Minimalista */}
        {loading && (
          <div className="text-center py-8">
            <div className="inline-block w-1 h-8 bg-black animate-pulse"></div>
          </div>
        )}

        {/* Results - Lista pulita, tipo terminale */}
        {results && !loading && (
          <div className="space-y-12">
            {Object.keys(results.results).length === 0 ? (
              <p className="text-gray-400 text-sm">nessun risultato</p>
            ) : (
              <>
                {Object.entries(results.results).map(([category, urls]) => (
                  <div key={category} className="group">
                    <div className="flex items-baseline gap-3 mb-3 sticky top-0 bg-white py-2">
                      <h2 className="text-xs uppercase tracking-wider text-gray-400 font-mono">
                        {category.replace(/_/g, " ")}
                      </h2>
                      <div className="flex-1 border-b border-gray-200"></div>
                      <span className="text-xs text-gray-400 font-mono">{urls.length}</span>
                    </div>
                    <ul className="space-y-1">
                      {urls.map((url, idx) => {
                        const { domain, path } = parseUrl(url);
                        return (
                          <li key={idx}>
                            <a
                              href={url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="block py-1 text-sm hover:translate-x-1 transition-all duration-150 group"
                            >
                              <span className="text-gray-900 group-hover:text-black font-medium">
                                {domain}
                              </span>
                              {path && (
                                <span className="text-gray-400 group-hover:text-gray-600 ml-1">
                                  {path}
                                </span>
                              )}
                            </a>
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                ))}
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
