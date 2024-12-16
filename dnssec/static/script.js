document.getElementById('query-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const domain = document.getElementById('domain').value;
    const resolver = document.getElementById('resolver').value || '34.27.111.125';
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<p>Tracing DNSSEC...</p>';
    
    fetch('/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            domain: domain,
            resolver: resolver 
        })
    })
    .then(response => response.json())
    .then(data => {
        resultsDiv.innerHTML = '';
        if (data.error) {
            resultsDiv.innerHTML = `<p>Error: ${data.error}</p>`;
        } else {
            visualizeDNSSECData(data);
        }
    })
    .catch(error => {
        resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
    });
});

function visualizeDNSSECData(data) {
    const resultsDiv = document.getElementById('results');
    
    if (data.length === 0) {
        resultsDiv.innerHTML = '<p>No DNSSEC trace data found.</p>';
        return;
    }

    const container = document.createElement('div');
    container.classList.add('dnssec-results');

    data.forEach((step, index) => {
        const stepDiv = document.createElement('div');
        stepDiv.classList.add('dnssec-step');
        
        // Domain name
        const domainHeader = document.createElement('h3');
        domainHeader.textContent = `Level: ${index} - ${step.qname || 'Unknown'}`;
        stepDiv.appendChild(domainHeader);

        // Validation details
        const validationDiv = document.createElement('div');
        validationDiv.classList.add('validation-details');

        // Record Validation
        const recordValidation = document.createElement('div');
        const recordType = step.type || 'Unknown';
        const recordData = step.data || 'No data';
        recordValidation.innerHTML = `
            <strong>${recordType} Record:</strong>
            <p>Data: ${recordData}</p>
        `;
        validationDiv.appendChild(recordValidation);

        stepDiv.appendChild(validationDiv);
        container.appendChild(stepDiv);
    });

    resultsDiv.appendChild(container);
}