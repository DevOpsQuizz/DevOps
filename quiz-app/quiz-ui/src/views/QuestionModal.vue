<script setup>
import { ref, watch, computed } from 'vue'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

const props = defineProps({
	open: Boolean,
	question: Object,
	onClose: Function,
	onSave: Function,
	quizSize: Number,
})

const local = ref({
	title: '',
	text: '',
	image: '',
	position: 1,
	possibleAnswers: [
		{ text: '', isCorrect: false },
		{ text: '', isCorrect: false },
	],
})

const imagePreview = ref('')

watch(() => props.open, (isOpen) => {
	if (!isOpen) {
		imagePreview.value = '' 
	}
})

watch(() => props.question, (q) => {
	if (q) {
		local.value = {
			title: q.title || '',
			text: q.text || '',
			image: q.image || '',
			position: q.position || 1,
			possibleAnswers: q.possibleAnswers?.map(a => ({ text: a.text, isCorrect: a.isCorrect })) || [
				{ text: '', isCorrect: false },
				{ text: '', isCorrect: false },
			],
		}
		imagePreview.value = q.image || '' 
	} else {
		local.value = {
			title: '',
			text: '',
			image: '',
			position: props.quizSize + 1,
			possibleAnswers: [
				{ text: '', isCorrect: false },
				{ text: '', isCorrect: false },
			],
		}
		imagePreview.value = '' 
	}
}, { immediate: true })

watch(() => local.value.image, (newImage) => {
	if (newImage) {
		imagePreview.value = newImage 
	}
}, { immediate: true })

function addAnswer() {
	local.value.possibleAnswers.push({ text: '', isCorrect: false })
}
function removeAnswer(idx) {
	if (local.value.possibleAnswers.length > 2) local.value.possibleAnswers.splice(idx, 1)
}
function setCorrect(idx) {
	local.value.possibleAnswers.forEach((a, i) => a.isCorrect = i === idx)
}
function handleSave() {
	if (!local.value.title.trim() || !local.value.text.trim()) return
	if (local.value.possibleAnswers.length < 2) return
	if (!local.value.possibleAnswers.some(a => a.isCorrect)) return
	props.onSave({ ...local.value })
}

function handleFileChange(event) {
	const file = event.target.files[0]
	if (file) {
		const reader = new FileReader()
		reader.onload = () => {
			imagePreview.value = reader.result 
			local.value.image = reader.result 
		}
		reader.readAsDataURL(file)
	}
}
</script>

<template>
	<div v-if="props.open" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
		<Card class="w-full max-w-xl p-6 relative">
			<CardHeader>
				<CardTitle class="text-2xl mb-2">{{ props.question ? 'Modifier la question' : 'Créer une question' }}</CardTitle>
			</CardHeader>
			<CardContent>
				<div class="flex flex-col gap-4">
					<Input v-model="local.title" placeholder="Titre de la question" class="text-lg" />
					<Input v-model="local.text" placeholder="Texte de la question" />
					<div class="mb-4">
						<label for="image" class="block text-sm font-medium text-gray-700">Image</label>
						<div v-if="imagePreview" class="mt-2">
							<img :src="imagePreview" alt="Preview" class="w-full h-auto max-h-64 object-contain border rounded" />
						</div>
						<input
							id="image"
							type="file"
							accept="image/*"
							class="mt-2 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
							@change="handleFileChange"
						/>
					</div>
								<div>
									<label class="font-medium mr-2">Position :</label>
									<select
										v-model="local.position"
										class="bg-gray-100 rounded px-2 py-1"
										:disabled="!props.question"
									>
										<option v-for="pos in props.quizSize" :key="pos" :value="pos">{{ pos }}</option>
										<option v-if="!props.question" :value="props.quizSize + 1">{{ props.quizSize + 1 }}</option>
									</select>
								</div>
					<div>
						<div class="font-medium mb-2">Réponses possibles :</div>
						<div class="flex flex-col gap-2">
							<div v-for="(a, idx) in local.possibleAnswers" :key="idx" class="flex items-center gap-2">
								<Input v-model="a.text" placeholder="Réponse" class="flex-1" />
								<input type="radio" :checked="a.isCorrect" @change="setCorrect(idx)" />
								<span class="text-green-600" v-if="a.isCorrect">Bonne réponse</span>
								<Button size="sm" variant="ghost" @click="removeAnswer(idx)" v-if="local.possibleAnswers.length > 2">🗑️</Button>
							</div>
							<Button size="sm" variant="outline" class="mt-2" @click="addAnswer">Ajouter une réponse</Button>
						</div>
					</div>
				</div>
			</CardContent>
			<CardFooter class="flex justify-end gap-2 mt-4">
				<Button variant="secondary" @click="props.onClose">Annuler</Button>
				<Button variant="default" @click="handleSave">Valider</Button>
			</CardFooter>
			<button @click="props.onClose" class="absolute top-2 right-2 text-xl">✖</button>
		</Card>
	</div>
</template>
