document.getElementById('exportBtn').addEventListener('click', () => {
    let url = document.querySelector('input[name="url"]').value;
    let keyword = document.querySelector('input[name="keyword"]').value;
    fetch(`/export?url=${encodeURIComponent(url)}&keyword=${encodeURIComponent(keyword)}`)
        .then(res => res.json())
        .then(data => alert(data.message))
        .catch(err => alert("Error exporting CSV"));
});
