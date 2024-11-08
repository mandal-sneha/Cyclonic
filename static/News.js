document.addEventListener("DOMContentLoaded", function() {
    const apiKey = "c35a5406889545269bc836d90ec9c376";
    const newsContainer = document.getElementById("news-container");

    const disasterKeywords = ["flood", "earthquake", "hurricane", "cyclone", "tsunami", "wildfire", "landslide", "eruption"];
    
    async function fetchDisasterNews() {
        try {
            const response = await fetch(`https://newsapi.org/v2/everything?q=${disasterKeywords.join(" OR ")}&language=en&sortBy=publishedAt&apiKey=${apiKey}`);
            const data = await response.json();

            if (data.status === "ok") {
                const filteredArticles = data.articles.filter(article => 
                    disasterKeywords.some(keyword => 
                        article.title.toLowerCase().includes(keyword) || 
                        article.description?.toLowerCase().includes(keyword)
                    ) && !article.title.toLowerCase().includes("football")
                );
                displayNews(filteredArticles);
            } else {
                newsContainer.innerHTML = "<p>Error fetching news.</p>";
            }
        } catch (error) {
            console.error("Error fetching news:", error);
            newsContainer.innerHTML = "<p>Unable to load news at the moment.</p>";
        }
    }

    function displayNews(articles) {
        newsContainer.innerHTML = ""; 

        if (articles.length === 0) {
            newsContainer.innerHTML = "<p>No relevant disaster news found.</p>";
            return;
        }

        articles.forEach(article => {
            const newsItem = document.createElement("div");
            newsItem.className = "news-item";

            newsItem.innerHTML = `
                ${article.urlToImage ? `<img src="${article.urlToImage}" alt="News Image" class="news-image">` : ""}
                <div class="news-content">
                    <h3><a href="${article.url}" target="_blank">${article.title}</a></h3>
                    <p>${article.description || "No description available"}</p>
                    <small>Source: ${article.source.name}</small>
                </div>
            `;

            newsContainer.appendChild(newsItem);
        });
    }

    fetchDisasterNews();
});