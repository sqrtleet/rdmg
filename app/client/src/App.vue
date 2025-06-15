<template>
  <div id="app">
    <!-- Фильтры и поиск -->
    <div class="controls">
      <label>
        Категория:
        <select v-model="filters.category">
          <option value="">Все</option>
          <option value="pothole">Pothole</option>
          <option value="crack">Crack</option>
        </select>
      </label>
      <label>
        Класс:
        <select v-model="filters.damage_class">
          <option value="">Все</option>
          <option value="minor">Minor</option>
          <option value="major">Major</option>
          <option value="critical">Critical</option>
        </select>
      </label>
      <label>
        Открытые:
        <select v-model="filters.is_open">
          <option value="">Все</option>
          <option :value="true">Open</option>
          <option :value="false">Closed</option>
        </select>
      </label>
      <label>
        Поиск по ID:
        <input v-model="searchId" @keyup.enter="resetFilters" placeholder="Enter ID…"/>
      </label>
      <button @click="resetFilters">Сбросить фильтры</button>
    </div>

    <div class="main">
      <!-- Карта -->
      <div id="map"></div>

      <!-- Список -->
      <div class="list">
        <ul>
          <li
              v-for="d in displayedDefects"
              :key="d.id"
              @click="selectDefect(d)"
          >
            <span
                class="marker-icon"
                :style="{ backgroundColor: getColor(d) }"
            ></span>
            {{ d.id }}
          </li>
        </ul>
      </div>
    </div>

    <!-- Детальная карточка -->
    <div
        class="detail-card"
        v-if="selectedDefect"
    >
      <h3>Defect ID: {{ selectedDefect.id }}</h3>
      <img
          :src="selectedDefect.image"
          alt="Defect image"
      />
      <p>
        Category:
        <select v-model="selectedDefect.category">
          <option value="pothole">Pothole</option>
          <option value="crack">Crack</option>
        </select>
      </p>
      <p>
        Damage class:
        <select v-model="selectedDefect.damage_class">
          <option value="minor">Minor</option>
          <option value="major">Major</option>
          <option value="critical">Critical</option>
        </select>
      </p>
      <p>
        Latitude: <input type="number" v-model.number="selectedDefect.latitude"/>
      </p>
      <p>
        Longitude:
        <input type="number" v-model.number="selectedDefect.longitude"/>
      </p>
      <p>
        Size:
        <input type="number" v-model.number="selectedDefect.size"/>
      </p>
      <label>
        Open:
        <input
            type="checkbox"
            v-model="selectedDefect.is_open"
        />
      </label>
      <div class="buttons">
        <button @click="saveDefect">Сохранить</button>
        <button @click="deleteDefect">Удалить</button>
        <button @click="closeDetail">Закрыть</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, reactive, computed, onMounted, watch} from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Состояние
const defects = ref([])
const selectedDefect = ref(null)
const filters = reactive({
  category: '',
  damage_class: '',
  is_open: ''
})
const searchId = ref('')

// Инициализация карты и маркеров
let map, markerGroup

onMounted(async () => {
  map = L.map('map').setView([61.98081, 129.66019], 15)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map)
  markerGroup = L.layerGroup().addTo(map)
  await loadDefects()
})

// Загрузка всех дефектов
async function loadDefects() {
  const res = await fetch('/api/defects/')
  defects.value = await res.json()
}

// Цвет маркера по категории
function getColor(d) {
  if (d.category === 'pothole') return 'crimson'
  if (d.category === 'crack') return 'darkorange'
  return 'gray'
}

// Вычисляемый список с учётом фильтров и поиска по ID
const displayedDefects = computed(() => {
  let list = defects.value

  // Поиск по ID
  if (searchId.value.trim()) {
    list = list.filter(d => d.id.includes(searchId.value.trim()))
  } else {
    if (filters.category)
      list = list.filter(d => d.category === filters.category)
    if (filters.damage_class)
      list = list.filter(d => d.damage_class === filters.damage_class)
    if (filters.is_open !== '')
      list = list.filter(d => d.is_open === filters.is_open)
  }
  return list
})

// Обновляем маркеры на карте при изменении списка
watch(displayedDefects, list => {
  markerGroup.clearLayers()
  list.forEach(d => {
    const m = L.circleMarker(
        [d.latitude, d.longitude],
        {
          radius: 6,
          fillColor: getColor(d),
          color: '#333',
          weight: 1,
          fillOpacity: 0.8
        }
    ).addTo(markerGroup)
    m.on('click', () => selectDefect(d))
  })
}, {immediate: true})

// Выбор дефекта
function selectDefect(d) {
  selectedDefect.value = {...d}   // создаём копию для редактирования
  map.setView([d.latitude, d.longitude])
}

// Сброс фильтров и поиска
function resetFilters() {
  filters.category = ''
  filters.damage_class = ''
  filters.is_open = ''
  searchId.value = ''
}

// Закрыть карточку
function closeDetail() {
  selectedDefect.value = null
}

// Сохранение изменений (PATCH)
async function saveDefect() {
  const d = selectedDefect.value
  await fetch(`/api/defects/${d.id}`, {
    method: 'PATCH',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      image: d.image,
      latitude: d.latitude,
      longitude: d.longitude,
      size: d.size,
      category: d.category,
      damage_class: d.damage_class,
      is_open: d.is_open
    })
  })
  await loadDefects()
  alert('Сохранено')
}

// Удаление (DELETE)
async function deleteDefect() {
  const id = selectedDefect.value.id
  await fetch(`/api/defects/${id}`, {method: 'DELETE'})
  selectedDefect.value = null
  await loadDefects()
  alert('Удалено')
}
</script>

<style>
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
  background-color: white;
}

#app {
  width: 100%;
  max-width: 90%;
  max-height: 900px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
  padding: 16px;
  box-sizing: border-box;
}

.controls {
  margin-bottom: 12px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.controls label {
  display: flex;
  flex-direction: column;
  font-size: 14px;
}

.controls label select, button, input, select {
  background-color: white;
  color: black;
}

button {
  border: 2px solid black;
  color: black;
}

button:hover {
  background: #e7e7e7;
}

.main {
  display: flex;
  gap: 12px;
}

#map {
  flex: 3;
  height: 700px;
  box-sizing: border-box;
  border: 1px solid #ccc;
}

.list {
  width: 20%;
  max-height: 700px;
  overflow-y: auto;
  border: 1px solid #ccc;
  padding: 8px;
}

.list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.list li {
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  color: black;
}

.list li + li {
  border-top: 1px solid #eee;
}

.marker-icon {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 8px;
}

.detail-card {
  position: fixed;
  top: 20px;
  right: 20px;
  width: 340px;
  background: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  padding: 16px;
  z-index: 1000;
  color: black;
}

.detail-card img {
  max-width: 100%;
  display: block;
  margin-bottom: 8px;
}

.detail-card .buttons {
  margin-top: 12px;
  display: flex;
  gap: 8px;
}
</style>
