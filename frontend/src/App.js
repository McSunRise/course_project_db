import React, { useState } from 'react';
import DataFetcher from './DataFetcher';
import CreateForm from './CreateForm';
import EditForm from './EditForm';
import SearchById from './SearchById';

function App() {
  const [selectedTable, setSelectedTable] = useState('clients');
  const [editingItem, setEditingItem] = useState(null);
  const [creating, setCreating] = useState(false);
  const [showTable, setShowTable] = useState(true);

  const handleEdit = (item) => {
    setEditingItem(item);
    setCreating(false);
    setShowTable(false);
  };

  const handleDelete = (item) => {
    if (!window.confirm('Удалить запись?')) return;

    fetch(`http://localhost:8000/api/${selectedTable}/${item.id}`, {
      method: 'DELETE',
    })
      .then((res) => {
        if (!res.ok) throw new Error(`Ошибка удаления: ${res.status}`);
        alert('Удалено успешно');
        setEditingItem(null);
        setShowTable(true);
      })
      .catch((err) => alert(err.message));
  };

  const handleBack = () => {
    setEditingItem(null);
    setCreating(false);
    setShowTable(true);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>📦 Панель управления БД</h1>

      <label>
        Выберите таблицу:
        <select
          value={selectedTable}
          onChange={(e) => {
            setSelectedTable(e.target.value);
            setShowTable(true);
            setEditingItem(null);
            setCreating(false);
          }}
          style={{ marginLeft: '10px' }}
        >
          <option value="clients">Клиенты</option>
          <option value="drivers">Водители</option>
          <option value="cars">Машины</option>
          <option value="orders">Заказы</option>
          <option value="staff">Сотрудники</option>
          <option value="positions">Должности</option>
          <option value="assignments">Назначения</option>
          <option value="orders_drivers">Заказы-водители</option>
          <option value="tech_inspection">Техосмотр</option>
        </select>
      </label>

      <SearchById
        table={selectedTable}
        onSelect={(item) => {
          setEditingItem(item);
          setCreating(false);
          setShowTable(false);
        }}
        onHideTable={() => setShowTable(false)}
      />

      {showTable && (
        <>
          <button onClick={() => setCreating(true)} style={{ marginTop: '10px' }}>
            ➕ Создать запись
          </button>
          <DataFetcher
            table={selectedTable}
            onEdit={handleEdit}
            onDelete={handleDelete}
          />
        </>
      )}

      {creating && (
        <>
          <h3>📝 Создание новой записи</h3>
          <CreateForm
            table={selectedTable}
            onSuccess={() => {
              setCreating(false);
            }}
          />
          <button onClick={handleBack} style={{ marginTop: '10px' }}>🔙 Назад</button>
        </>
      )}

      {editingItem && (
        <>
          <EditForm
            table={selectedTable}
            item={editingItem}
            onSuccess={() => {
              setEditingItem(null);
              setShowTable(true);
            }}
          />
          <button
            onClick={() => handleDelete(editingItem)}
            style={{ marginTop: '10px', marginRight: '10px', color: 'red' }}
          >
            🗑️ Удалить запись
          </button>
          <button onClick={handleBack}>🔙 Назад</button>
        </>
      )}
    </div>
  );
}

export default App;
