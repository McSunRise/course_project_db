import React, { useState, useEffect, forwardRef, useImperativeHandle } from 'react';

const DataFetcher = forwardRef(({ table, onEdit, onDelete }, ref) => {
  const [data, setData] = useState([]);

  const fetchData = () => {
    fetch(`http://localhost:8000/api/${table}`)
      .then(res => res.json())
      .then(setData)
      .catch(console.error);
  };

  useEffect(fetchData, [table]);

  useImperativeHandle(ref, () => ({
    refresh: fetchData
  }));

  if (!data.length) return <p>Нет данных.</p>;

  return (
    <table border="1" cellPadding="5" style={{ marginTop: '10px' }}>
      <thead>
        <tr>
          {Object.keys(data[0]).map((key) => (
            <th key={key}>{key}</th>
          ))}
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item) => (
          <tr key={item.id}>
            {Object.values(item).map((val, idx) => (
              <td key={idx}>{val}</td>
            ))}
            <td>
              <button onClick={() => onEdit(item)}>✏️</button>{' '}
              <button onClick={() => onDelete(item)}>🗑️</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
});

export default DataFetcher;
