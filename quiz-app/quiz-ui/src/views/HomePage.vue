<script setup>
import { ref, watch, onMounted } from 'vue'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'

const playerName = ref('')
const showQuiz = ref(false)

const question = ref(null)
const loading = ref(false)
const error = ref(null)

const currentQuestion = ref(0)
const totalQuestions = ref(0)
const answers = ref(Array(totalQuestions.value).fill(null))
const selectedOption = ref(null)

async function fetchQuestion(position) {
  loading.value = true
  error.value = null
  try {
    const res = await fetch(`http://127.0.0.1:5000/api/questions/quiz?position=${position + 1}`)
    if (!res.ok) throw new Error('Erreur lors du chargement')
    question.value = await res.json()
  } catch (e) {
    error.value = e.message
    question.value = null
  } finally {
    loading.value = false
  }
}

async function fetchTotalQuestions() {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/questions/count')
    if (!res.ok) throw new Error('Erreur lors du comptage')
    const data = await res.json()
    totalQuestions.value = data.count
    answers.value = Array(totalQuestions.value).fill(null)
  } catch (e) {
    error.value = e.message
    totalQuestions.value = 0
  }
}

// Charger le nombre total de questions au montage
onMounted(async () => {
  await fetchTotalQuestions()
})

// Surveiller le changement de question pour charger la nouvelle question via l'API
watch(currentQuestion, async (newIndex) => {
  selectedOption.value = answers.value[newIndex]
  await fetchQuestion(newIndex)
})

/**
 * Enregistre la réponse et passe à la question suivante
 */
async function nextQuestion() {
  answers.value[currentQuestion.value] = selectedOption.value
  if (currentQuestion.value < totalQuestions.value - 1) {
    currentQuestion.value++
  }
}

/**
 * Va à la question spécifiée si elle a déjà été répondue
 */
function goToQuestion(index) {
  if (answers.value[index] !== null) {
    currentQuestion.value = index
  }
}

/**
 * Démarre le quiz si un nom d'utilisateur a été saisi
 */
async function startQuiz() {
  if (playerName.value.trim() !== '') {
    showQuiz.value = true
    currentQuestion.value = 0
    answers.value = Array(totalQuestions.value).fill(null)
    selectedOption.value = null
    await fetchQuestion(0)
  }
}
</script>

<template>
  <section class="flex flex-col items-center justify-center min-h-screen bg-white">
    <div v-if="!showQuiz" class="flex flex-col items-center space-y-6">
      <h1 class="text-3xl font-semibold mb-4">Prêt pour le meilleur quiz de tout les temps ?</h1>
      <input
        v-model="playerName"
        type="text"
        placeholder="Nom d'utilisateur ..."
        class="rounded-lg px-6 py-3 bg-gray-100 text-xl placeholder-gray-400 focus:outline-none"
        style="min-width: 320px;"
      />
      <Button
        class="bg-gray-300 text-xl px-8 py-2 mt-2"
        :disabled="playerName.trim() === ''"
        @click="startQuiz"
      >
        C'est parti !
      </Button>
    </div>

    <div v-else class="w-full">
      <section class="flex flex-row p-12 space-x-8 items-start">
        <!-- Bloc réponse aux questions -->
        <Card class="flex-1 max-w-2xl bg-gray-100">
          <CardHeader>
            <CardTitle class="text-2xl mb-2">Lorem ipsum dolor (Theme du quiz)</CardTitle>
          </CardHeader>
          <CardContent>
            <div v-if="loading" class="text-center my-8">Chargement…</div>
            <div v-else-if="error" class="text-red-500 my-8">{{ error }}</div>
            <div v-else-if="question" class="mb-4">
              <div class="font-semibold mb-1">Question N°{{ currentQuestion + 1 }}</div>
              <img
                v-if="question.image"
                :src="question.image"
                alt="illustration"
                class="w-full max-h-64 object-cover rounded my-4"
              />
              <div class="mb-4">{{ question.text }}</div>
              <RadioGroup v-model="selectedOption" class="space-y-4">
                <div
                  v-for="(option, index) in question.answers"
                  :key="option.id"
                  class="flex items-center space-x-4"
                >
                  <RadioGroupItem
                    :value="index"
                    :id="'option-' + index"
                    class="w-6 h-6 border-2 border-gray-300"
                  />
                  <label :for="'option-' + index" class="text-base cursor-pointer w-full">
                    {{ option.text }}
                  </label>
                </div>
              </RadioGroup>
            </div>
            <div class="flex justify-center mt-8">
              <Button
                class="bg-gray-300 text-xl px-8 py-2"
                :disabled="selectedOption === null"
                @click="nextQuestion"
              >
                Suivant <span class="ml-2 text-2xl">→</span>
              </Button>
            </div>
          </CardContent>
        </Card>

        <!-- Bloc navigation questions -->
        <Card class="w-72 bg-gray-100">
          <CardHeader>
            <CardTitle class="text-lg">Questions</CardTitle>
          </CardHeader>
          <CardContent class="space-y-3">
            <div
              v-for="index in totalQuestions"
              :key="index"
              class="flex items-center justify-between px-4 py-3 rounded-lg transition-all"
              :class="{
                'bg-gray-200 text-gray-400 cursor-not-allowed': answers[index - 1] === null,
                'bg-white hover:bg-blue-100 cursor-pointer': answers[index - 1] !== null
              }"
              @click="goToQuestion(index - 1)"
            >
              <span>Question N°{{ index }}</span>
              <span v-if="answers[index - 1] !== null" class="w-3 h-3 bg-green-700 rounded-full inline-block"></span>
            </div>
          </CardContent>
        </Card>
      </section>
    </div>
  </section>
</template>