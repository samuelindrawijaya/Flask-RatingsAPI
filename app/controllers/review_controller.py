from flask import jsonify, request
from app.DAL.review_Dal import ReviewDAL

class ReviewController:
    @staticmethod
    def get_all_reviews():
        """
        Get all reviews
        ---
        tags:
          - Reviews
        security:
          - bearerAuth: []
        responses:
          200:
            description: A list of reviews
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: Review ID
                    example: 1
                  content:
                    type: string
                    description: Review content
                    example: "Great product!"
                  user_id:
                    type: integer
                    description: User ID
                    example: 1
          500:
            description: Internal Server Error
        """
        reviews = ReviewDAL.list_reviews()
        return jsonify([review.to_dict() for review in reviews]), 200

    @staticmethod
    def get_review_by_id(review_id):
        """
        Get review by ID
        ---
        tags:
          - Reviews
        security:
          - bearerAuth: []
        parameters:
          - name: review_id
            in: path
            required: true
            schema:
              type: integer
              example: 1
        responses:
          200:
            description: Review found
            schema:
              type: object
              properties:
                id:
                  type: integer
                  description: Review ID
                  example: 1
                content:
                  type: string
                  description: Review content
                  example: "Great product!"
                user_id:
                  type: integer
                  description: User ID
                  example: 1
          404:
            description: Review not found
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Review not found"
        """
        review = ReviewDAL.get_review_by_id(review_id)
        if review:
            return jsonify(review.to_dict()), 200
        return jsonify({'message': 'Review not found'}), 404

    @staticmethod
    def add_review():
        """
        Add a new review
        ---
        tags:
          - Reviews
        security:
          - bearerAuth: []
        parameters:
          - name: review
            in: body
            required: true
            schema:
              type: object
              properties:
                content:
                  type: string
                  description: Review content
                  example: "This is a great product!"
                user_id:
                  type: integer
                  description: User ID
                  example: 1
        responses:
          201:
            description: Review created successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Review created successfully."
                review:
                  type: object
                  properties:
                    id:
                      type: integer
                      description: Review ID
                      example: 1
                    content:
                      type: string
                      description: Review content
                      example: "Great product!"
                    user_id:
                      type: integer
                      description: User ID
                      example: 1
          400:
            description: Review content or user ID is missing
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Review content and user ID are required"
        """
        data = request.get_json()
        if not data or 'content' not in data or 'user_id' not in data:
            return jsonify({'message': 'Review content and user ID are required'}), 400

        review = ReviewDAL.create_review(data['content'], data['user_id'])
        return jsonify({
            'message': "Review created successfully.",
            'review': review.to_dict()
        }), 201

    @staticmethod
    def update_review(review_id):
        """
        Update a review
        ---
        tags:
          - Reviews
        security:
          - bearerAuth: []
        parameters:
          - name: review_id
            in: path
            required: true
            schema:
              type: integer
              example: 1
          - name: review
            in: body
            required: true
            schema:
              type: object
              properties:
                content:
                  type: string
                  description: Review content
                  example: "Updated review content"
        responses:
          200:
            description: Review updated successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Review updated successfully."
                review:
                  type: object
                  properties:
                    id:
                      type: integer
                      description: Review ID
                      example: 1
                    content:
                      type: string
                      description: Updated review content
                      example: "Updated review content"
                    user_id:
                      type: integer
                      description: User ID
                      example: 1
          400:
            description: Review content is required
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Review content is required"
          404:
            description: Review not found
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Review not found"
        """
        data = request.get_json()
        if not data or 'content' not in data:
            return jsonify({'message': 'Review content is required'}), 400

        review = ReviewDAL.update_review(review_id, data['content'])
        if review:
            return jsonify({
                'message': "Review updated successfully.",
                'review': review.to_dict()
            }), 200
        return jsonify({'message': 'Review not found'}), 404

    @staticmethod
    def delete_review(review_id):
        """
        Delete a review
        ---
        tags:
          - Reviews
        security:
          - bearerAuth: []
        parameters:
          - name: review_id
            in: path
            required: true
            schema:
              type: integer
              example: 1
        responses:
          200:
            description: Review deleted successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Review deleted successfully."
          404:
            description: Review not found
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Review not found"
        """
        deleted = ReviewDAL.delete_review(review_id)
        if deleted:
            return jsonify({'message': 'Review deleted successfully.'}), 200
        return jsonify({'message': 'Review not found'}), 404
