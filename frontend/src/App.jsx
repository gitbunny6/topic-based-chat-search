import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // New state for chat uploading
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");
  const [uploadError, setUploadError] = useState("");

  async function handleUpload(event) {
    event.preventDefault();

    if (!file) {
      setUploadError("Please choose a WhatsApp .txt file first.");
      setUploadMessage("");
      return;
    }

    if (!file.name.toLowerCase().endsWith(".txt")) {
      setUploadError("Please select a WhatsApp .txt file, not a ZIP file.");
      setUploadMessage("");
      return;
    }

    setUploading(true);
    setUploadError("");
    setUploadMessage("");
    setResults([]);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Chat upload failed.");
      }

      setUploadMessage(
        `Successfully uploaded ${data.filename}. Processed ${data.messages_processed} messages and indexed ${data.chunks_indexed} chunks. You can now search this chat.`
      );
      setFile(null);

      // Reset the file input after a successful upload
      event.target.reset();
    } catch (err) {
      setUploadError(
        err.message || "Could not connect to the backend server."
      );
    } finally {
      setUploading(false);
    }
  }

  async function handleSearch(event) {
    event.preventDefault();

    if (!query.trim()) return;

    setLoading(true);
    setError("");
    setResults([]);

    try {
      const response = await fetch(`${API_URL}/search`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: query,
          top_k: 5,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Search request failed.");
      }

      setResults(data.results);
    } catch (err) {
      setError(
        "Could not connect to the search server. Please check that the backend is running."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        background: "#101116",
        color: "#f5f4fa",
        minHeight: "100vh",
        padding: "60px 20px",
        fontFamily: "Arial, sans-serif",
        textAlign: "center",
      }}
    >
      <h2 style={{ color: "#b49aff" }}>ChatSearch</h2>

      <h1 style={{ fontSize: "52px", marginTop: "60px" }}>
        Find the meaning,
        <br />
        not just the <span style={{ color: "#b49aff" }}>words.</span>
      </h1>

      <p style={{ color: "#aaa", lineHeight: 1.8 }}>
        Search your chat history by topic or idea.
        <br />
        Let AI find the conversations that matter.
      </p>

      {/* New chat upload section */}
      <form
        onSubmit={handleUpload}
        style={{
          maxWidth: "650px",
          margin: "30px auto",
          padding: "22px",
          background: "#1b1b24",
          border: "1px solid #333",
          borderRadius: "12px",
          textAlign: "left",
        }}
      >
        <h3 style={{ marginTop: 0 }}>Upload your WhatsApp chat</h3>

        <p style={{ color: "#aaa", fontSize: "14px", lineHeight: 1.6 }}>
          Choose an exported WhatsApp .txt file to make its conversations
          searchable.
        </p>

        <input
          type="file"
          accept=".txt,text/plain"
          onChange={(event) => {
            setFile(event.target.files?.[0] || null);
            setUploadMessage("");
            setUploadError("");
          }}
          style={{
            display: "block",
            width: "100%",
            margin: "18px 0",
            color: "#ddd",
          }}
        />

        <button
          type="submit"
          disabled={uploading}
          style={{
            padding: "12px 20px",
            borderRadius: "8px",
            border: 0,
            background: uploading ? "#555" : "#8460e8",
            color: "white",
            cursor: uploading ? "wait" : "pointer",
          }}
        >
          {uploading ? "Uploading and processing..." : "Upload Chat ↑"}
        </button>

        {uploadMessage && (
          <p style={{ color: "#8ee6ae", lineHeight: 1.6 }}>
            {uploadMessage}
          </p>
        )}

        {uploadError && (
          <p style={{ color: "#ff8080", lineHeight: 1.6 }}>
            {uploadError}
          </p>
        )}
      </form>

      {/* Existing search section */}
      <form
        onSubmit={handleSearch}
        style={{
          display: "flex",
          gap: "10px",
          maxWidth: "650px",
          margin: "35px auto",
        }}
      >
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Try searching for internship..."
          style={{
            flex: 1,
            minWidth: 0,
            padding: "16px",
            borderRadius: "10px",
            border: "1px solid #444",
            background: "#20202a",
            color: "white",
            fontSize: "16px",
          }}
        />

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: "16px 24px",
            borderRadius: "10px",
            border: 0,
            background: "#8460e8",
            color: "white",
            cursor: "pointer",
          }}
        >
          {loading ? "Searching..." : "Search →"}
        </button>
      </form>

      <p style={{ color: "#888" }}>AI-powered semantic chat search</p>

      {loading && (
        <p style={{ color: "#b49aff" }}>
          Searching your conversations...
        </p>
      )}

      {error && <p style={{ color: "#ff8080" }}>{error}</p>}

      {!loading && results.length > 0 && (
        <section
          style={{
            maxWidth: "750px",
            margin: "35px auto",
            textAlign: "left",
          }}
        >
          <h2>Search Results ({results.length})</h2>

          {results.map((result, index) => (
            <article
              key={index}
              style={{
                background: "#1b1b24",
                border: "1px solid #333",
                borderRadius: "12px",
                padding: "20px",
                marginBottom: "14px",
              }}
            >
              <p style={{ color: "#b49aff", fontSize: "13px" }}>
                Match {index + 1} · Similarity:{" "}
                {Number(result.score).toFixed(3)}
              </p>

              <p
                style={{
                  lineHeight: 1.7,
                  whiteSpace: "pre-wrap",
                  overflowWrap: "anywhere",
                }}
              >
                {result.text}
              </p>

              <p style={{ color: "#999", fontSize: "12px" }}>
                {result.start_time
                  ? new Date(result.start_time).toLocaleString()
                  : ""}
                {" · "}
                {result.message_count} messages
              </p>
            </article>
          ))}
        </section>
      )}

      {!loading && !error && query.trim() && results.length === 0 && (
        <p style={{ color: "#aaa" }}>
          No results yet. Try another search.
        </p>
      )}

      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: "12px",
          flexWrap: "wrap",
          marginTop: "55px",
        }}
      >
        {[
          "Meaning-based search",
          "Conversation context",
          "AI-powered retrieval",
        ].map((item) => (
          <div
            key={item}
            style={{
              background: "#1b1b24",
              border: "1px solid #333",
              borderRadius: "12px",
              padding: "25px",
              minWidth: "190px",
            }}
          >
            {item}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;