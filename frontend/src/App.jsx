import { useState, useEffect } from "react";
import axios from "axios";
import "./styles.css";

function App() {
    const [longUrl, setLongUrl] = useState("");
    const [shortUrl, setShortUrl] = useState("");
    const [urls, setUrls] = useState([]);

    useEffect(() => {
        axios.get("http://localhost:5000/api/urls").then((response) => {
            setUrls(response.data);
        });
    }, [shortUrl]);

    const handleShorten = async () => {
        const response = await axios.post("http://localhost:5000/api/shorten", { long_url: longUrl });
        setShortUrl(response.data.short_url);
    };

    return (
        <div className="container">
            <h1>🔗 URL Shortener</h1>
            <input
                type="text"
                placeholder="Enter a long URL"
                value={longUrl}
                onChange={(e) => setLongUrl(e.target.value)}
            />
            <button onClick={handleShorten}>Shorten URL</button>

            {shortUrl && (
                <p>
                    Shortened URL: <a href={`http://localhost:5000/${shortUrl}`} target="_blank" rel="noopener noreferrer">{`http://localhost:5000/${shortUrl}`}</a>
                </p>
            )}

            <h2>📌 All Shortened URLs</h2>
            <ul>
                {urls.map((url, index) => (
                    <li key={index}>
                        <a href={`http://localhost:5000/${url.short_url}`} target="_blank" rel="noopener noreferrer">
                            {`http://localhost:5000/${url.short_url}`}
                        </a>{" "}
                        → {url.long_url}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;
