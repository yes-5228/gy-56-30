<template>
  <article class="route-card">
    <div class="route-head">
      <div>
        <p class="eyebrow">{{ route.city }} · {{ route.days }} 天</p>
        <h3>{{ route.title }}</h3>
      </div>
      <span class="tag">{{ route.status_label }}</span>
    </div>
    <p class="description">{{ route.description }}</p>
    <div class="budget-grid">
      <span>基础费用 <b>¥{{ route.base_cost }}</b></span>
      <span>门票合计 <b>¥{{ route.ticket_total }}</b></span>
      <span>预计总价 <b>¥{{ route.estimated_cost }}</b></span>
    </div>
    <div class="progress-row">
      <span>已报名 {{ route.enrolled_count }}/{{ route.min_group_size }}</span>
      <div class="progress-track">
        <i :style="{ width: `${route.group_progress}%` }"></i>
      </div>
    </div>
    <div v-if="route.review_count > 0" class="rating-row">
      <div class="rating-info">
        <span class="rating-score">{{ route.average_rating }}</span>
        <span class="rating-stars">
          <i v-for="n in 5" :key="n" :class="{ filled: n <= Math.round(route.average_rating) }">★</i>
        </span>
        <span class="rating-count">{{ route.review_count }} 条评价</span>
      </div>
    </div>
    <ol class="stop-list">
      <li v-for="stop in route.stops" :key="stop.id">
        <span>D{{ stop.day }}-{{ stop.order }}</span>
        <div>
          <b>{{ stop.attraction.name }}</b>
          <p>{{ stop.note }}</p>
        </div>
      </li>
    </ol>
    <div v-if="route.reviews && route.reviews.length > 0" class="review-section">
      <h4>游客反馈</h4>
      <ul class="review-list">
        <li v-for="review in route.reviews.slice(0, 3)" :key="review.id" class="review-item">
          <div class="review-head">
            <span class="reviewer">{{ review.reviewer_name }}</span>
            <span class="review-rating">
              <i v-for="n in 5" :key="n" :class="{ filled: n <= review.rating }">★</i>
            </span>
          </div>
          <p v-if="review.feedback" class="review-feedback">{{ review.feedback }}</p>
        </li>
      </ul>
    </div>
    <button
      v-if="route.can_review"
      type="button"
      class="review-action"
      @click="$emit('open-review', route)"
    >
      提交评价
    </button>
  </article>
</template>

<script setup>
defineProps({
  route: { type: Object, required: true },
});

defineEmits(["open-review"]);
</script>
