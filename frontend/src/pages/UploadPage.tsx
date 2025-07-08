import { useState } from "react";
import type { FormEvent, DragEvent } from "react";
import { useNavigate } from "react-router-dom";
import { Lightbulb, FileText, UploadCloud, Loader2, X } from "lucide-react";
import { motion } from "framer-motion";
const API_BASE_URL = "/api";

export default function UploadPage() {
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [resumeText, setResumeText] = useState("");
  const [jobDescription, setJobDescription] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (files: FileList | null) => {
    setError(null);
    if (files && files[0]) {
      const file = files[0];
      if (file.type !== "application/pdf" && !file.name.endsWith(".txt")) {
        setError("Only PDF or TXT files are allowed.");
        setResumeFile(null);
        return;
      }
      setResumeFile(file);
      setResumeText("");
    }
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
    handleFileChange(e.dataTransfer.files);
  };

  const handleDragEvents = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setIsDragOver(true);
    } else if (e.type === "dragleave") {
      setIsDragOver(false);
    }
  };

  const handleResumeTextChange = (
    e: React.ChangeEvent<HTMLTextAreaElement>
  ) => {
    setError(null);
    setResumeText(e.target.value);
    if (e.target.value) {
      setResumeFile(null);
    }
  };

  async function handleAnalyze(event: FormEvent) {
    event.preventDefault();
    setError(null);

    if ((!resumeFile && !resumeText.trim()) || !jobDescription.trim()) {
      setError("Please provide a resume (file or text) and a job description.");
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("job_description", jobDescription);

      let endpoint = "";

      if (resumeFile) {
        endpoint = `${API_BASE_URL}/analyze-resume`;
        formData.append("resume_file", resumeFile);
      } else {
        endpoint = `${API_BASE_URL}/analyze-resume-text`;
        formData.append("resume_text", resumeText);
      }

      const resp = await fetch(endpoint, {
        method: "POST",
        body: formData,
      });

      if (!resp.ok) {
        const errorData = await resp.json().catch(() => ({
          detail:
            "Analysis failed. The server may be busy or an error occurred.",
        }));
        throw new Error(errorData.detail || "An unknown error occurred.");
      }

      const data = await resp.json();
      navigate("/dashboard", { state: { analysisData: data } });
    } catch (err: any) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <main className="flex flex-col justify-center items-center min-h-[calc(100vh-4rem)] py-8 px-4">
        <motion.form
          onSubmit={handleAnalyze}
          className="bg-white p-8 rounded-2xl shadow-lg max-w-2xl w-full space-y-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <h2 className="text-3xl font-bold text-gray-800 mb-4 text-center flex items-center gap-3 justify-center">
            <FileText className="text-blue-600 w-8 h-8" />
            Analyze Candidate Fit
          </h2>

          {/* File Upload Section */}
          <div
            onDrop={handleDrop}
            onDragEnter={handleDragEvents}
            onDragOver={handleDragEvents}
            onDragLeave={handleDragEvents}
            className={`relative border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors duration-200 ease-in-out
              ${
                isDragOver
                  ? "border-blue-500 bg-blue-50"
                  : "border-gray-300 bg-gray-50 hover:border-blue-400"
              }`}
          >
            <input
              type="file"
              accept=".pdf, .txt"
              onChange={(e) => handleFileChange(e.target.files)}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              id="resume-upload"
              disabled={!!resumeText}
            />
            <label
              htmlFor="resume-upload"
              className="flex flex-col items-center justify-center space-y-2"
            >
              <UploadCloud className="w-10 h-10 text-gray-400" />
              <p className="text-gray-600">
                <span className="font-semibold text-blue-600">
                  Click to upload
                </span>{" "}
                or drag and drop
              </p>
              <p className="text-xs text-gray-500">PDF or TXT files only</p>
            </label>
          </div>

          {resumeFile && (
            <div className="flex items-center justify-between bg-gray-100 p-2 rounded-md text-sm">
              <p className="text-gray-700 truncate">{resumeFile.name}</p>
              <button
                onClick={() => setResumeFile(null)}
                className="text-gray-500 hover:text-red-600"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          )}

          {/* Separator */}
          <div className="flex items-center">
            <div className="flex-grow border-t border-gray-300"></div>
            <span className="flex-shrink mx-4 text-gray-400 font-semibold">
              OR
            </span>
            <div className="flex-grow border-t border-gray-300"></div>
          </div>

          {/* Text Input Section */}
          <div>
            <label
              htmlFor="resume-text"
              className="font-medium text-gray-700 block mb-2"
            >
              Paste Resume Text
            </label>
            <textarea
              id="resume-text"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 focus:outline-none resize-y min-h-[120px] transition"
              placeholder="Paste the full resume text here..."
              value={resumeText}
              onChange={handleResumeTextChange}
              disabled={!!resumeFile}
            />
          </div>

          {/* Job Description Section */}
          <div>
            <label
              htmlFor="job-description"
              className="font-medium text-gray-700 block mb-2"
            >
              Job Description
            </label>
            <textarea
              id="job-description"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 focus:outline-none resize-y min-h-[120px] transition"
              placeholder="Paste the job description here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              required
            />
          </div>

          {error && (
            <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-3 rounded-r-lg text-sm text-center">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full flex justify-center items-center gap-3 bg-blue-600 text-white px-6 py-3 rounded-full font-semibold text-lg hover:bg-blue-700 transition-all duration-300 disabled:bg-blue-400 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <Loader2 className="w-6 h-6 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Lightbulb className="w-6 h-6" />
                Analyze Now
              </>
            )}
          </button>
        </motion.form>
      </main>
    </div>
  );
}
