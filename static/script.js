
const keywordForm = document.getElementById("keyword-form");
const keywordBox = document.getElementById("keyword-box");


function displayArticles(data) {
    
    console.log("DISPLAY ARTICLES RECEIVED:", data)

    const articleTable = document.getElementById("article-table");

    articleTable.innerHTML = "";

    if (data.length === 0) {
        articleTable.innerHTML = "<tr><td colspan='9'>No Results Found</td></tr>";
        return;
    }

    data.forEach(article => {

        
        const row = document.createElement("tr");
        const title = document.createElement("td");
        title.textContent = article.title;

        const author = document.createElement("td");
        author.textContent = article.author;

        const description = document.createElement("td");
        description.textContent = article.description;

        const country = document.createElement("td");
        country.textContent = article.country;

        const publishedAt = document.createElement("td");
        publishedAt.textContent = article.publishedAt;

        const content = document.createElement("td");
        content.textContent = article.content;

        const source = document.createElement("td");
        source.textContent = article["source.name"];

        const url = document.createElement("td");
        url.textContent = article.url;

        const keywords = document.createElement("td");
        keywords.textContent = article.Keywords.join(", ");

        row.appendChild(title);
        row.appendChild(author);
        row.appendChild(description);
        row.appendChild(country);
        row.appendChild(publishedAt);
        row.appendChild(content);
        row.appendChild(source);
        row.appendChild(url);
        row.appendChild(keywords);


        articleTable.appendChild(row);

    });
}

const searchForm = document.getElementById("search-form");


searchForm.addEventListener("submit", function(event) {
    event.preventDefault();


    const formData = new FormData(searchForm);

    fetch("/search", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    //.then(response => response.text())
    .then(data => {
        
        //console.log("REMOVE RESPONSE:", data)
        displayArticles(data);
        //displayArticles(data.articles);
                
    });



    
});



function displayKeywords(data) {

    keywordBox.innerHTML = "";

    data.forEach(word => {

        const keyword = document.createElement("div");
        keyword.classList.add("keyword");

        const keywordText = document.createElement("p");
        keywordText.textContent = word;

        // "Remove" Button function
        const removeButton = document.createElement("button");
        removeButton.textContent = "x";
        
        removeButton.addEventListener("click", function() {
            console.log("Remove button clicked!", word);
            
            const formData = new FormData();
            
            formData.append("keyword", word);

            fetch("/keyword-remove", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {

                console.log(data);
               // displayArticles(data.keyword_exclusion_list);
        

            });
        });

        keyword.appendChild(keywordText);
        keyword.appendChild(removeButton);

        keywordBox.appendChild(keyword);
    });

}



keywordForm.addEventListener("submit", function(event) {
    event.preventDefault();

    console.log("KEYWORD FORM SUBMITTED!");
    
    const formData = new FormData(keywordForm);

    console.log("SENDING KEYWORD FILTER REQUEST");

    fetch("/keyword-filter", {
    method: "POST",
    body: formData
    })
    .then(response => response.json())
    //.then(response => response.text())
    .then(data => {
        
        console.log("KEYWORD FILTER RESPONSE:",data);
        console.log("FILTERED ARTICLES:", data.articles);

        displayArticles(data.articles);
        displayKeywords(data.keyword_exclusion_list);

    });
    
    
});