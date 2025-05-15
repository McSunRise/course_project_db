import React, { useState } from 'react';

function EditForm({ table, item, onSuccess, onCancel }) {
  const [formData, setFormData] = useState({ ...item });
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch(`http://localhost:8000/api/${table}/${item.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    })
      .then(res => {
        if (!res.ok) throw new Error('Ошибка при обновлении');
        return res.json();
      })
      .then(() => {
        onSuccess();
        onCancel();
      })
      .catch(err => setError(err.message));
  };

  const handleDelete = () => {
    if (!window.confirm('Вы уверены, что хотите удалить эту запись?')) return;
    fetch(`http://localhost:8000/api/${table}/${item.id}`, {
      method: 'DELETE'
    })
      .then(res => {
        if (!res.ok) throw new Error('Ошибка при удалении');
        onSuccess();
        onCancel();
      })
      .catch(err => setError(err.message));
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '10px', marginTop: '20px' }}>
      <h3>Редактирование записи #{item.id}</h3>
      <form onSubmit={handleSubmit}>
        {Object.keys(formData).map((key) => (
          key !== 'id' && (
            <div key={key} style={{ marginBottom: '10px' }}>
              <label>{key}: </label>
              <input
                type="text"
                name={key}
                value={formData[key]}
                onChange={handleChange}
              />
            </div>
          )
        ))}
        <button type="submit">Сохранить</button>{' '}
        <button type="button" onClick={onCancel}>Отмена</button>{' '}
        <button type="button" onClick={handleDelete} style={{ color: 'red' }}>
          Удалить
        </button>
      </form>
      {error && <p style={{ color: 'red' }}>Ошибка: {error}</p>}
    </div>
  );
}

export default EditForm;
