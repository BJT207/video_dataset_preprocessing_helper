import cv2
from tqdm import tqdm


class ImageSelector:
    def __init__(self, images):
        self.images = images
        self.image_fm = self._compute_sharpness_values()

    def _compute_sharpness_values(self):
        print("Calculating image sharpness...")
        return [(self.variance_of_laplacian(cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2GRAY)), img) for img in tqdm(self.images)]

    @staticmethod
    def variance_of_laplacian(image):
        return cv2.Laplacian(image, cv2.CV_64F).var()

    @staticmethod
    def distribute_evenly(total, num_of_groups):
        ideal_per_group = total / num_of_groups
        accumulated_error = 0.0
        distribution = [0] * num_of_groups

        for i in range(num_of_groups):
            distribution[i] = int(ideal_per_group)
            accumulated_error += ideal_per_group - distribution[i]

            while accumulated_error >= 1.0:
                distribution[i] += 1
                accumulated_error -= 1.0

        return distribution

    def filter_sharpest_images(self, target_count, group_count=None, scalar=1):
        if scalar is None:
            scalar = 1
        if group_count is None:
            group_count = target_count // (2 ** (scalar - 1))
            group_count = max(1, group_count)

        group_sizes = self.distribute_evenly(len(self.images), group_count)

        images_per_group_list = self.distribute_evenly(target_count, group_count)

        selected_images = []
        offset_index = 0
        for idx, size in enumerate(group_sizes):
            end_idx = offset_index + size
            group = sorted(self.image_fm[offset_index:end_idx], reverse=True)
            selected_images.extend([img[1] for img in group[:images_per_group_list[idx]]])
            offset_index = end_idx

        return selected_images
