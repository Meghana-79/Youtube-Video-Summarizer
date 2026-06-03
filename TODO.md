- [x] Implement robust transcript extraction + better errors in utils/transcript.py
- [x] Add debug logging + structured TranscriptResult to utils/transcript.py
- [ ] Update Flask /api/summarize in app.py to return consistent JSON success:false {message, code, details}
- [ ] Map youtube-transcript-api exceptions to frontend error codes/messages
- [ ] Ensure Flask validates URL formats before extraction
- [ ] Update templates/index.html frontend JS: stepwise loading messages + code-based error display
- [ ] Add optional lightweight endpoint for debugging transcript availability (if needed)
- [ ] Run quick local test: /health, /api/summarize with known good URL(s)
- [ ] Verify browser console/network: no 400/404 for valid requests; correct UI error messages for invalid/caption-disabled videos



