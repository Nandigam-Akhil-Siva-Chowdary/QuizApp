import cloudinary.uploader


class CloudinaryService:
    """
    Centralized Cloudinary upload helper.
    """

    @staticmethod
    def upload_pdf(*, file_bytes, filename):
        """
        Upload a PDF file to Cloudinary.
        """

        result = cloudinary.uploader.upload(
            file_bytes,
            resource_type="raw",
            public_id=filename.replace(".pdf", ""),
            format="pdf"
        )

        return {
            "secure_url": result.get("secure_url"),
            "public_id": result.get("public_id"),
        }

    @staticmethod
    def upload_image(*, file_bytes, filename):
        """
        Upload an image (PNG/JPG) to Cloudinary.
        """

        result = cloudinary.uploader.upload(
            file_bytes,
            resource_type="image",
            public_id=filename
        )

        return {
            "secure_url": result.get("secure_url"),
            "public_id": result.get("public_id"),
        }
