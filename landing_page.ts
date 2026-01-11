
import React, { useRef, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Upload, Sparkles, Download, Workflow } from "lucide-react";
import { motion } from "framer-motion";

export default function LandingPage() {
  const [jobId, setJobId] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [done, setDone] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInput = useRef<HTMLInputElement>(null);

  // Upload CSV handler
  const handleUpload = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setUploading(true);
    setProcessing(false);
    setDone(false);
    setJobId(null);
    const form = e.currentTarget;
    const file = fileInput.current?.files?.[0];
    if (!file) {
      setError("Please select a CSV file.");
      setUploading(false);
      return;
    }
    const data = new FormData();
    data.append("file", file);
    try {
      const res = await fetch("/api/jobs/upload", {
        method: "POST",
        body: data,
      });
      if (!res.ok) throw new Error("Upload failed");
      const json = await res.json();
      setJobId(json.job_id);
      setUploading(false);
      setProcessing(true);
      // Start profiling (triggers pipeline)
      await fetch(`/api/jobs/${json.job_id}/profile`, { method: "POST" });
      // Poll for job status
      let status = "profiling";
      while (["profiling", "suggesting", "applying"].includes(status)) {
        await new Promise((r) => setTimeout(r, 1500));
        const resp = await fetch(`/api/jobs/${json.job_id}`);
        const job = await resp.json();
        status = job.status;
      }
      setProcessing(false);
      setDone(true);
    } catch (err: any) {
      setError(err.message || "Unknown error");
      setUploading(false);
      setProcessing(false);
    }
  };
      {/* Hero */}
      <section className="max-w-6xl mx-auto px-6 py-20 text-center">
        <form onSubmit={handleUpload} className="mb-8 flex flex-col items-center gap-4">
          <input
            type="file"
            accept=".csv"
            ref={fileInput}
            className="border rounded px-3 py-2"
            disabled={uploading || processing}
          />
          <Button type="submit" size="lg" disabled={uploading || processing}>
            {uploading ? "Uploading..." : processing ? "Processing..." : "Upload & Clean CSV"}
          </Button>
        </form>
        {error && <div className="text-red-500 mb-2">{error}</div>}
        {done && jobId && (
          <div className="flex flex-col items-center gap-2 mb-4">
            <a
              href={`/api/jobs/${jobId}/download`}
              className="text-blue-600 underline flex items-center gap-1"
              download
            >
              <Download size={18} /> Download Cleaned CSV
            </a>
            <a
              href={`/api/jobs/${jobId}/report`}
              className="text-blue-600 underline flex items-center gap-1"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Sparkles size={18} /> View Cleaning Report
            </a>
          </div>
        )}
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-4xl md:text-5xl font-bold mb-6"
        >
          AI Data Cleaning Assistant
        </motion.h1>
        <p className="text-lg md:text-xl text-gray-600 mb-8">
          Upload raw CSV data. Get clean, analysis-ready datasets automatically.
        </p>
        <div className="flex justify-center gap-4">
          <Button size="lg" asChild>
            <a href="#how">How it works</a>
          </Button>
          <Button variant="outline" size="lg" asChild>
            <a href="https://github.com/your-repo" target="_blank" rel="noopener noreferrer">View Docs</a>
          </Button>
        </div>
      </section>

      {/* How it works */}
      <section className="max-w-6xl mx-auto px-6 py-16 grid md:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6 text-center">
            <Upload className="mx-auto mb-4" />
            <h3 className="font-semibold mb-2">Upload CSV</h3>
            <p className="text-sm text-gray-600">Submit raw, messy datasets.</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6 text-center">
            <Workflow className="mx-auto mb-4" />
            <h3 className="font-semibold mb-2">Profile & Analyze</h3>
            <p className="text-sm text-gray-600">Automatic data profiling.</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6 text-center">
            <Sparkles className="mx-auto mb-4" />
            <h3 className="font-semibold mb-2">AI Cleaning</h3>
            <p className="text-sm text-gray-600">LLM-generated cleaning steps.</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6 text-center">
            <Download className="mx-auto mb-4" />
            <h3 className="font-semibold mb-2">Download Clean Data</h3>
            <p className="text-sm text-gray-600">Ready for analytics or ML.</p>
          </CardContent>
        </Card>
      </section>

      {/* Why */}
      <section className="bg-white py-20">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold mb-6">Why this tool?</h2>
          <p className="text-gray-600 mb-4">
            Built with production-grade architecture: FastAPI, MCP, and n8n.
            Designed to be safe, reproducible, and scalable.
          </p>
          <p className="text-gray-600">
            No notebooks. No manual cleaning. Just automated pipelines.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-10 text-center text-sm text-gray-500">
        © 2026 AI Data Cleaning Assistant · Built for AI Dev Tools Zoomcamp
      </footer>
    </div>
  );
}
