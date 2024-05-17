import React, { useState, useEffect } from 'react';
import axios from 'axios';
import editIcon from '../images/edit_image.png';
import deleteIcon from '../images/bin.jpg'; // Импортируем изображение корзины
import '.././App.css'; // Импортируем стили из App.css

function CountriesPage() {
  const [countries, setCountries] = useState([]);
  const [newCountryName, setNewCountryName] = useState('');
  const [editedCountryName, setEditedCountryName] = useState('');
  const [editingCountryId, setEditingCountryId] = useState(null);
  const [selectedCountries, setSelectedCountries] = useState([]); // Массив для хранения выбранных стран

  // Функция для получения списка стран с сервера
  async function fetchCountries() {
    try {
      const response = await axios.get('http://127.0.0.1:5000/country');
      setCountries(response.data.countries);
    } catch (error) {
      console.error('Error fetching countries:', error);
    }
  }

  // Функция для добавления новой страны
  async function addCountry() {
    try {
      const formData = new URLSearchParams();
      formData.append('name', newCountryName);

      await axios.post('http://127.0.0.1:5000/add_country', formData.toString(), {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });

      // После успешного добавления обновляем список стран
      fetchCountries();
      // Сбрасываем значение новой страны
      setNewCountryName('');
    } catch (error) {
      console.error('Error adding country:', error);
    }
  }

  // Функция для редактирования страны
  async function editCountry(countryId) {
    try {
      const updatedCountry = {
        name: editedCountryName
      };
  
      await axios.put(`http://127.0.0.1:5000/update_country/${countryId}`, updatedCountry, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
  
      // После успешного редактирования обновляем список стран
      fetchCountries();
      // Сбрасываем значения
      setEditingCountryId(null);
      setEditedCountryName('');
    } catch (error) {
      console.error('Error editing country:', error);
    }
  }

  // Функция для удаления страны (или выбранных стран)
  async function deleteCountries() {
    try {
      // Если выбраны страны, удаляем только выбранные, иначе удаляем одну редактируемую страну
      const countryIdsToDelete = selectedCountries.length > 0 ? selectedCountries : [editingCountryId];
      
      await Promise.all(countryIdsToDelete.map(async countryId => {
        await axios.delete(`http://127.0.0.1:5000/delete_country/${countryId}`);
      }));

      // После успешного удаления обновляем список стран
      fetchCountries();
      // Сбрасываем выбранные страны и редактируемую страну
      setSelectedCountries([]);
      setEditingCountryId(null);
    } catch (error) {
      console.error('Error deleting countries:', error);
    }
  }

  // Обработчик для выделения страны
  function handleCountrySelect(countryId) {
    if (selectedCountries.includes(countryId)) {
      setSelectedCountries(selectedCountries.filter(id => id !== countryId)); // Удаляем из массива
    } else {
      setSelectedCountries([...selectedCountries, countryId]); // Добавляем в массив
    }
  }

  useEffect(() => {
    fetchCountries();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h2>List of Countries</h2>
        <ul>
          {countries.map((country, index) => (
            <li key={index} className={`country-item ${selectedCountries.includes(country.id) ? 'selected' : ''}`} onClick={() => handleCountrySelect(country.id)}>
              {editingCountryId === country.id ? (
                <div>
                  <input
                    type="text"
                    value={editedCountryName}
                    onChange={(e) => setEditedCountryName(e.target.value)}
                    placeholder="Enter edited country name"
                  />
                  <button className="save-btn" onClick={() => editCountry(country.id)}>Save</button>
                </div>
              ) : (
                <div className="buttons-right">
                  <span>{country.name}</span>
                  <div>
                    <button className="edit-btn" onClick={() => setEditingCountryId(country.id)}>
                      <img src={editIcon} alt="Edit" className="edit-icon" />
                    </button>
                  </div>
                </div>
              )}
            </li>
          ))}
        </ul>
        <div>
          <input
            type="text"
            value={newCountryName}
            onChange={(e) => setNewCountryName(e.target.value)}
            placeholder="Enter new country name"
          />
          <button className="add-btn" onClick={addCountry}>Add Country</button>
        </div>
        <div>
          {/* Кнопка для удаления выбранных стран */}
          <button className="delete-btn" onClick={deleteCountries}>
          <img src={deleteIcon} alt="Delete" className="delete-icon" style={{ width: '100px', height: 'auto' }} />
          </button>
        </div>
      </header>
    </div>
  );
}

export default CountriesPage;

