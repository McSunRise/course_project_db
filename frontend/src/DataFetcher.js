import React, { useEffect, useState } from 'react';

function DataFetcher({ table, reload, onSelectRow }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const url = `http://localhost:8000/api/${table}`;

  useEffect(() => {
    setData(null);
    fetch(url)
      .then(response => {
        if (!response.ok) throw new Error(`Ошибка: ${response.status}`);
        return response.json();
      })
      .then(json => setData(json))
      .catch(err => setError(err.message));
  }, [table, reload]);

  if (error) return <div>❌ Ошибка: {error}</div>;
  if (!data) return <div>⏳ Загрузка...</div>;
  if (!Array.isArray(data)) return <pre>{JSON.stringify(data, null, 2)}</pre>;

  return (
    <div style={{ marginTop: '20px' }}>
      <h2>Содержимое {table}</h2>
      <table border="1" cellPadding="8" style={{ borderCollapse: 'collapse', cursor: 'pointer' }}>
        <thead>
          <tr>
            {Object.keys(data[0] || {}).map((key) => (
              <th key={key}>{key}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((item) => (
            <tr
              key={item.id || JSON.stringify(item)}
              onClick={() => onSelectRow?.(item)} // ✅ Безопасный вызов
              style={{ backgroundColor: '#f9f9f9' }}
            >
              {Object.keys(item).map((key) => (
                <td key={key}>{String(item[key])}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <p style={{ marginTop: '10px' }}>💡 Нажмите на запись, чтобы изменить её</p>
    </div>
  );
}

export default DataFetcher;
