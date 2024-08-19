import { useEffect, useState } from 'react'
import { GoogleGenerativeAI } from '@google/generative-ai'
import { GEN_AI_KEY } from './config'
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
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', backgroundColor: '#f5f5f5', justifyContent: 'center' }}>
    <div style={{
      width: '90%',
      maxWidth: '800px', // Optional: Limit maximum width for larger screens
      margin: '0 auto',
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
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
        <Typography variant="h4" component="h1" gutterBottom>
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
        <form onSubmit={handleSubmit} style={{ display: 'flex',marginBottom:"10px", gap: '16px' }}>
          <TextField
            variant="outlined"
            label="Ask a question"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            fullWidth
            style={{
              borderRadius: '20px', // Rounded corners
              transition: 'all 0.3s ease-in-out', // Smooth transition
            }}
            InputProps={{
              style: {
                borderRadius: '20px', // Rounded corners for input
              },
            }}
            InputLabelProps={{
              style: {
                borderRadius: '20px', // Rounded corners for label
              },
            }}
            sx={{
              '& .MuiOutlinedInput-root': {
                '& fieldset': {
                  borderRadius: '20px', // Rounded corners for fieldset
                },
                '&:hover fieldset': {
                  borderColor: 'blue', // Focus border color
                },
                '&.Mui-focused fieldset': {
                  borderColor: 'blue', // Focus border color
                },
              },
            }}
          />

          {/* <Button
            type="submit"
            variant="contained"
            color="primary"
            size='medium'
            disabled={loading}
            style={{
              borderRadius: '20px', // Rounded corners
              fontSize: '0.875rem', // Smaller font size
              minWidth: '18px', // Remove default minimum width
              transition: 'background-color 0.3s ease, transform 0.2s ease', // Smooth transitions
              boxShadow: loading ? 'none' : '0px 4px 6px rgba(0, 0, 0, 0.1)',
            }}

            sx={{
              '&:hover': {
                backgroundColor: '#1976d2', // Darker blue on hover
                transform: 'scale(1.05)', // Slight scale effect on hover
              },
              '&.Mui-disabled': {
                backgroundColor: '#e0e0e0', // Disabled button color
                color: '#b0b0b0',
              },
            }}
          >
            {loading ? <CircularProgress size={24} /> : 'Submit'}
          </Button> */}
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
