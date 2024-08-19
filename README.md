# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh


 <div style={{ marginTop: '40px' }}>
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
        </div>
