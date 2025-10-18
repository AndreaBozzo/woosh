"use client";

import { useState } from "react";

interface SearchResults {
  results: Record<string, string[]>;
  total: number;
}

interface VATInfo {
  country_code: string;
  vat_number: string;
  is_valid: boolean;
  company_name?: string;
  company_address?: string;
  request_date?: string;
  error_message?: string;
}

type SearchMode = "name" | "vat";

export default function Home() {
  const [mode, setMode] = useState<SearchMode>("name");
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<SearchResults | null>(null);
  const [vatInfo, setVatInfo] = useState<VATInfo | null>(null);
  const [error, setError] = useState("");

  async function handleNameSearch() {
    if (!query.trim()) {
      setError("insert enterprise name or VAT");
      return;
    }

    setLoading(true);
    setError("");
    setResults(null);
    setVatInfo(null);

    try {
      const res = await fetch(`/api/search?query=${encodeURIComponent(query)}&max_results=100`);

      if (!res.ok) {
        throw new Error("error during research");
      }

      const data = await res.json();
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "error during research");
    } finally {
      setLoading(false);
    }
  }

  async function handleVATSearch() {
    if (!query.trim()) {
      setError("insert VAT number");
      return;
    }

    setLoading(true);
    setError("");
    setResults(null);
    setVatInfo(null);

    try {
      const res = await fetch(`/api/vat/${encodeURIComponent(query)}`);

      if (!res.ok) {
        throw new Error("error during validation");
      }

      const data = await res.json();
      setVatInfo(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "error during validation");
    } finally {
      setLoading(false);
    }
  }

  function handleSearch() {
    if (mode === "name") {
      handleNameSearch();
    } else {
      handleVATSearch();
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
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-3xl mx-auto px-4 py-12 sm:py-16">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-4xl sm:text-5xl font-light tracking-tight mb-2 text-gray-900">woosh</h1>
          <p className="text-gray-500 text-sm">Company Search Tool</p>
        </div>

        {/* Mode Toggle */}
        <div className="mb-8 flex gap-4 text-sm">
          <button
            onClick={() => {
              setMode("name");
              setQuery("");
              setResults(null);
              setVatInfo(null);
              setError("");
            }}
            className={`px-0 pb-1 border-b-2 transition-colors ${
              mode === "name"
                ? "border-black text-black"
                : "border-transparent text-gray-400 hover:text-gray-600"
            }`}
          >
            per nome
          </button>
          <button
            onClick={() => {
              setMode("vat");
              setQuery("");
              setResults(null);
              setVatInfo(null);
              setError("");
            }}
            className={`px-0 pb-1 border-b-2 transition-colors ${
              mode === "vat"
                ? "border-black text-black"
                : "border-transparent text-gray-400 hover:text-gray-600"
            }`}
          >
            with VAT number
          </button>
        </div>

        {/* Search Input */}
        <div className="mb-8">
          <div className="max-w-xl bg-white rounded-lg shadow-sm border border-gray-200 p-5">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              placeholder={mode === "name" ? "enter company name..." : "enter VAT number..."}
              className="w-full px-0 py-2 text-base bg-transparent border-0 focus:outline-none placeholder:text-gray-400"
              autoFocus
            />
            {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
          </div>
        </div>

        {/* Loading */}
        {loading && (
          <div className="text-center py-8">
            <div className="inline-block w-1 h-8 bg-black animate-pulse"></div>
          </div>
        )}

        {/* VAT Results */}
        {vatInfo && !loading && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            {vatInfo.is_valid ? (
              <>
                <div className="flex items-baseline gap-3 mb-4 pb-3 border-b border-gray-100">
                  <h2 className="text-xs uppercase tracking-wider text-gray-500 font-mono">
                    infos
                  </h2>
                  <div className="flex-1"></div>
                  <span className="text-xs text-green-600 font-medium">valid</span>
                </div>
                <div className="space-y-3 text-sm">
                  <div className="flex">
                    <span className="text-gray-400 w-32">country</span>
                    <span className="text-gray-900">{vatInfo.country_code}</span>
                  </div>
                  <div className="flex">
                    <span className="text-gray-400 w-32">VAT number</span>
                    <span className="text-gray-900 font-mono">{vatInfo.vat_number}</span>
                  </div>
                  {vatInfo.company_name && (
                    <div className="flex">
                      <span className="text-gray-400 w-32">company</span>
                      <span className="text-gray-900">{vatInfo.company_name}</span>
                    </div>
                  )}
                  {vatInfo.company_address && (
                    <div className="flex">
                      <span className="text-gray-400 w-32">address</span>
                      <span className="text-gray-900">{vatInfo.company_address}</span>
                    </div>
                  )}
                </div>
              </>
            ) : (
              <div>
                <div className="flex items-baseline gap-3 mb-4 pb-3 border-b border-gray-100">
                  <h2 className="text-xs uppercase tracking-wider text-gray-500 font-mono">
                    risultato
                  </h2>
                  <div className="flex-1"></div>
                  <span className="text-xs text-red-600 font-medium">non valida</span>
                </div>
                {vatInfo.error_message && (
                  <p className="text-sm text-gray-600">{vatInfo.error_message}</p>
                )}
              </div>
            )}
          </div>
        )}

        {/* Name Search Results */}
        {results && !loading && (
          <div className="space-y-6">
            {Object.keys(results.results).length === 0 ? (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 text-center">
                <p className="text-gray-400 text-sm">nessun risultato</p>
              </div>
            ) : (
              <>
                {Object.entries(results.results).map(([category, urls]) => (
                  <div key={category} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <div className="flex items-baseline gap-3 mb-4 pb-3 border-b border-gray-100">
                      <h2 className="text-xs uppercase tracking-wider text-gray-500 font-mono">
                        {category.replace(/_/g, " ")}
                      </h2>
                      <div className="flex-1"></div>
                      <span className="text-xs text-gray-400 font-mono">{urls.length}</span>
                    </div>
                    <ul className="space-y-2">
                      {urls.map((url, idx) => {
                        const { domain, path } = parseUrl(url);
                        return (
                          <li key={idx}>
                            <a
                              href={url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="block py-2 px-3 -mx-3 text-sm rounded hover:bg-gray-50 transition-colors group"
                            >
                              <span className="text-gray-900 group-hover:text-black font-medium">
                                {domain}
                              </span>
                              {path && (
                                <span className="text-gray-500 group-hover:text-gray-700 ml-1 text-xs">
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
