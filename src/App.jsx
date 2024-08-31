import { useEffect, useState } from 'react'
import { GoogleGenerativeAI } from '@google/generative-ai'
import './index.css'
import {
  TextField,
  Button,
  Typography,
  Paper,
  CircularProgress,
  Snackbar,
  Alert,
  Skeleton,
  List,
  ListItem,
  ListItemText
} from '@mui/material';
const genAI = new GoogleGenerativeAI(import.meta.env.VITE_GEN_AI_KEY);

function App() {
  const [answer, setAnswer] = useState("");
  const [error, setError] = useState("");
  const [question, setQuestion] = useState("");
  const [history, setHistory] = useState([]);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 500);
  const [loading, setLoading] = useState(false);
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    setError("");
    setAnswer("");

    try {
      const model = genAI.getGenerativeModel({
        model: "gemini-1.5-pro", // Replace with an actual valid model name
      });

      const response = await model.generateContent(question);

      const responseText = response.response.text();

      setAnswer(responseText);
      setQuestion("")
      // Update history with the new question and answer
      setHistory(prevHistory => [
        ...prevHistory,
        { question, answer: responseText }
      ]);


    } catch (err) {
      console.error("Error:", err);
      setError("Failed to fetch the answer.");
    } finally {
      setLoading(false);
    }
  };
  // useEffect(() => {
  //   const getModel = async () => {
  //     try {
  //       // const model = await genAI.listModels(); // Adjust to the correct method
  //       // console.log("Available models:", model);

  //       const generativeModel = genAI.getGenerativeModel({
  //         model: "gemini-1.5-pro" // Update with a valid model name
  //       });

  //       const response = await generativeModel.generateContent("The Capital of India");
  //       setAnswer(response.response.text);
  //     } catch (err) {
  //       console.error("Error:", err);
  //       setError("Failed to fetch the model or generate content.");
  //     }
  //   };

  //   getModel();
  // }, []);
  const handleSnackbarClose = () => {
    setOpenSnackbar(false);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: isMobile ? '100vh' : '100vh', backgroundColor: '#f5f5f5', justifyContent: 'center' }}>
      <div style={{
        width: isMobile ? "100%" : 'auto',
        maxWidth: '800px',
        margin: '0 auto',
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        maxHeight: isMobile ? '100%' : 'none',
        overflowY: isMobile ? 'auto' : 'hidden',
        borderRadius: '8px',
        overflow: 'hidden',
      }}>
        {/* History Display */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '16px', backgroundColor: '#ffffff', borderBottom: '1px solid #ddd' }}>
          <Paper
            elevation={3}
            style={{
              padding: '20px',
              marginBottom: '20px',
              boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
            }}
          >
            <Typography variant="h5" component="h2" gutterBottom>
              History
            </Typography>
            <List>
              {history.length > 0 ? (
                history.map((item, index) => (
                  <ListItem key={index} style={{ borderBottom: '1px solid #ddd' }}>
                    <ListItemText
                      primary={`Q: ${item.question}`}
                      secondary={`A: ${item.answer}`}
                    />
                  </ListItem>
                ))
              ) : (
                <Typography variant="body1" color="textSecondary">
                  No history available.
                </Typography>
              )}
            </List>
          </Paper>
          <Typography variant={isMobile ? "h5" : "h4"} component="h1" gutterBottom>
            Generative AI Integration
          </Typography>

          {loading ? (
            <Skeleton variant="rectangular" width="100%" height={100} animation="wave" />
          ) : answer ? (
            <Paper
              elevation={3}
              style={{
                padding: '20px',
                borderRadius: '8px',
                marginBottom: '20px',
              }}
              className="answer-paper"
            >
              <Typography variant="h6" component="h2">
                Answer:
              </Typography>
              <Typography variant="body1">
                {answer}
              </Typography>
            </Paper>
          ) : (
            <Typography variant="body1" color="textSecondary">
              Ask a question to get an answer.
            </Typography>
          )}
        </div>

        {/* Fixed Input Area */}
        <div style={{ padding: '16px', borderTop: '1px solid #ddd', backgroundColor: '#ffffff' }}>
          <form onSubmit={handleSubmit} style={{ display: 'flex',justifyContent:"center",  gap: '10px', alignItems: 'flex-end' }}>
            <TextField
              variant="outlined"
              label="Ask a question"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              fullWidth
              style={{
                borderRadius: '20px',
                transition: 'all 0.3s ease-in-out',
                paddingRight: isMobile ? '5px' : '10px', // Add some padding to the right
              }}
              InputProps={{
                style: {
                  borderRadius: '20px',
               
                },
              }}
              InputLabelProps={{
                style: {
                  borderRadius: '20px',
                },
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderRadius: '20px',
                  },
                  '&:hover fieldset': {
                    borderColor: 'blue',
                  },
                  '&.Mui-focused fieldset': {
                    borderColor: 'blue',
                  },
                },
              }}
            />

            {/* Show the button only on mobile devices */}
            {isMobile && (
              <Button
                type="submit"
                variant="contained"
                color="primary"
                size="small"
                disabled={loading}
                style={{
                  borderRadius: '10px',
                  marginBottom:"10px",
                  fontSize: '0.875rem',
                  minWidth: '80px', // Set a minimum width for better appearance
                  padding: '6px 12px', // Adjust padding for a balanced look
                  transition: 'background-color 0.3s ease, transform 0.2s ease',
                  boxShadow: loading ? 'none' : '0px 4px 6px rgba(0, 0, 0, 0.1)',
                  marginLeft: '10px', // Add margin to separate the button from the text field
                }}
              >
                {loading ? <CircularProgress size={20} /> : 'Search'}
              </Button>
            )}
          </form>

        </div>
      </div>

      <Snackbar
        open={openSnackbar}
        autoHideDuration={6000}
        onClose={handleSnackbarClose}
        message="Failed to fetch the answer"
      >
        <Alert onClose={handleSnackbarClose} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>
    </div>

  );
}

export default App
