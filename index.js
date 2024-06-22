function fetchGitHubData() {
    fetch('/fetch_github_data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            alert('GitHub data fetched and saved to database!');
            console.log(data);  // Optional: log response data
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            alert('Error fetching GitHub contributions. Please try again.');
        });
}
