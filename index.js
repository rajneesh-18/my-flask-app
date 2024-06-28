// app/static/js/main.js
function fetchGitHubData() {
    fetch('/fetch_github_data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            alert('GitHub data fetched and saved to the database!');
            console.log(data);  // Optional: log response data

            // Process and display GitHub contributions
            const contributionsSection = document.getElementById('contributions');
            contributionsSection.innerHTML = '';  // Clear any existing content

            data.forEach(repo => {
                const repoElement = document.createElement('div');
                repoElement.className = 'col-md-4 mb-4';
                repoElement.innerHTML = `
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">${repo.name}</h5>
                            <p class="card-text">${repo.description}</p>
                            <a href="${repo.html_url}" class="btn btn-primary" target="_blank">View on GitHub</a>
                        </div>
                    </div>
                `;
                contributionsSection.appendChild(repoElement);
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            alert('Error fetching GitHub contributions. Please try again.');
        });
}
