<script setup>
import { ref } from 'vue'
import axios from 'axios'

const input = ref('')
const messages = ref([])

const sendMessage = async () => {
  if (!input.value.trim()) return;

  messages.value.push({ from: 'user', text: input.value })

  try {
    const res = await axios.post('http://localhost:8000/ask', {
      user: "demo_user",
      content: input.value
    })

    messages.value.push({ from: 'bot', text: res.data.response })
  } catch (err) {
    messages.value.push({ from: 'bot', text: "Hata oluştu: " + err.message })
  }

  input.value = ''
}
</script>

<template>
  <div>
    <div v-for="msg in messages" :key="msg.text">
      <b>{{ msg.from }}:</b> {{ msg.text }}
    </div>
    <input v-model="input" @keyup.enter="sendMessage" />
    <button @click="sendMessage">Gönder</button>
  </div>
</template>
