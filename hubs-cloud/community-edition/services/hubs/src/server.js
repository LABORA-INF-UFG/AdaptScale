const express = require('express');
const app = express();
const port = 9100;

app.get('/metrics', (req, res) => {
  res.send('Métricas estão funcionando!');
});

app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`);
});

