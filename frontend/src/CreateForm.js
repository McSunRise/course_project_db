import React, { useState, useEffect } from 'react';

function CreateForm({ table, onSuccess }) {
  const [formData, setFormData] = useState({});
  const [fields, setFields] = useState([]);
  const [error, setError] = useState(null);

  // Загружаем пример записи, чтобы определить поля
  useEffect(() => {
    fetch(`http://localhost:8000/api/${table}`)
      .then(res => res.json())
      .then(data => {
        const firstItem = data[0] || {};
        const keys = Object.keys(firstItem).filter(k => k !== 'id');
        const initialForm = {};
        keys.forEach(key => initialForm[key] = '');
        setFields(keys);
        setFormData(initialForm);
      });
  }, [table]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch(`http://localhost:8000/api/${table}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData)
    })
      .then(res => {
        if (!res.ok) throw new Error('Ошибка при создании');
        return res.json();
      })
      .then(() => {
        onSuccess(); // перезагрузить список
        setFormData(fields.reduce((obj, key) => ({ ...obj, [key]: '' }), {}));
      })
      .catch(err => setError(err.message));
  };

  if (!fields.length) return <div>Загрузка полей...</div>;

  return (
    <div style={{ marginTop: '20px' }}>
      <h3>Добавить запись в таблицу: {table}</h3>
      <form onSubmit={handleSubmit}>
        {fields.map(field => (
          <div key={field} style={{ marginBottom: '10px' }}>
            <label>{field}: </label>
            <input
              type="text"
              name={field}
              value={formData[field]}
              onChange={handleChange}
              required
            />
          </div>
        ))}
        <button type="submit">Добавить</button>
      </form>
      {error && <p style={{ color: 'red' }}>Ошибка: {error}</p>}
    </div>
  );
}

export default CreateForm;
