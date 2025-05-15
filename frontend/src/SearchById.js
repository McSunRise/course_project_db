import React, { useState } from 'react';

function SearchById({ table, onSelect, onHideTable }) {
  const [id, setId] = useState('');

  const handleSearch = () => {
    if (!id) return alert('Введите ID');

    fetch(`http://localhost:8000/api/${table}/${id}`)
      .then((res) => {
        if (!res.ok) throw new Error(`Ошибка ${res.status}`);
        return res.json();
      })
      .then((data) => {
        if (!data || (Array.isArray(data) && data.length === 0)) {
          alert('Запись не найдена');
          return;
        }

        // Если пришёл массив, берём первый элемент
        const item = Array.isArray(data) ? data[0] : data;

        onSelect(item);
        onHideTable();
      })
      .catch((err) => alert(err.message));
  };

  return (
    <div style={{ marginTop: '20px' }}>
      <h3>🔍 Поиск по ID</h3>
      <input
        type="number"
        placeholder="ID"
        value={id}
        onChange={(e) => setId(e.target.value)}
      />
      <button onClick={handleSearch} style={{ marginLeft: '10px' }}>Найти</button>
    </div>
  );
}

export default SearchById;
