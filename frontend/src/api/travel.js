import { get, post } from "./http";

export const travelApi = {
  getAttractions: () => get("/attractions/"),
  getRoutes: () => get("/routes/"),
  getBookings: () => get("/bookings/"),
  getNotices: () => get("/notifications/"),
  createBooking: (payload) => post("/bookings/", payload),
  getRouteReviews: (routeId) => get(`/routes/${routeId}/reviews/`),
  createRouteReview: (routeId, payload) => post(`/routes/${routeId}/reviews/`, payload),
};
