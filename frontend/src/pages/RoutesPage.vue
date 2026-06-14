<template>
  <section class="page-stack">
    <div class="metrics-row">
      <MetricCard label="线路数量" :value="routes.length" hint="覆盖多目的地线路" />
      <MetricCard label="成团中" :value="formingCount" hint="持续收客线路" />
      <MetricCard label="平均预算" :value="averageBudget" hint="按线路预计总价" />
    </div>
    <div class="route-grid">
      <RouteCard v-for="route in routes" :key="route.id" :route="route" @open-review="openReviewModal" />
    </div>
    <div v-if="reviewModalVisible" class="review-modal-backdrop" @click.self="closeReviewModal">
      <div class="review-modal">
        <h3>评价「{{ currentRoute?.title }}」</h3>
        <label>
          <span>您的姓名</span>
          <input v-model="reviewForm.reviewer_name" type="text" placeholder="请输入姓名" />
        </label>
        <label>
          <span>评分</span>
          <div class="star-picker">
            <button
              v-for="n in 5"
              :key="n"
              type="button"
              :class="{ filled: n <= reviewForm.rating }"
              @click="reviewForm.rating = n"
            >
              ★
            </button>
          </div>
        </label>
        <label>
          <span>反馈内容（选填）</span>
          <textarea v-model="reviewForm.feedback" rows="4" placeholder="分享您的旅行体验..."></textarea>
        </label>
        <div class="modal-actions">
          <button type="button" class="cancel-btn" @click="closeReviewModal">取消</button>
          <button type="button" class="submit-btn" @click="submitReview" :disabled="!reviewForm.reviewer_name || !reviewForm.rating">
            提交评价
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, reactive, ref } from "vue";
import { travelApi } from "../api/travel";
import MetricCard from "../components/MetricCard.vue";
import RouteCard from "../components/RouteCard.vue";

const props = defineProps({
  routes: { type: Array, required: true },
});

const emit = defineEmits(["review-submitted"]);

const reviewModalVisible = ref(false);
const currentRoute = ref(null);
const reviewForm = reactive({
  reviewer_name: "",
  rating: 5,
  feedback: "",
});

const formingCount = computed(() => props.routes.filter((route) => route.status === "forming").length);
const averageBudget = computed(() => {
  if (!props.routes.length) return "¥0";
  const total = props.routes.reduce((sum, route) => sum + Number(route.estimated_cost), 0);
  return `¥${Math.round(total / props.routes.length)}`;
});

function openReviewModal(route) {
  currentRoute.value = route;
  reviewForm.reviewer_name = "";
  reviewForm.rating = 5;
  reviewForm.feedback = "";
  reviewModalVisible.value = true;
}

function closeReviewModal() {
  reviewModalVisible.value = false;
  currentRoute.value = null;
}

async function submitReview() {
  if (!currentRoute.value || !reviewForm.reviewer_name || !reviewForm.rating) return;
  try {
    await travelApi.createRouteReview(currentRoute.value.id, {
      reviewer_name: reviewForm.reviewer_name,
      rating: reviewForm.rating,
      feedback: reviewForm.feedback,
    });
    closeReviewModal();
    emit("review-submitted");
  } catch (err) {
    alert(`提交失败：${err.message}`);
  }
}
</script>
