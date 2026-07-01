import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Get the package share directory
    pkg_share = get_package_share_directory('mediapipe_ros')

    # 2. Declare Launch Arguments
    label_path_default = os.path.join(pkg_share, 'model', 'keypoint_classifier', 'keypoint_classifier_label.csv')
    model_path_default = os.path.join(pkg_share, 'model', 'keypoint_classifier', 'keypoint_classifier.tflite')

    keypoint_classifier_label_cmd = DeclareLaunchArgument(
        'keypoint_classifier_label',
        default_value=label_path_default,
        description='Path to the keypoint classifier label CSV (Gesture names)'
    )

    keypoint_classifier_model_cmd = DeclareLaunchArgument(
        'keypoint_classifier_model',
        default_value=model_path_default,
        description='Path to the keypoint classifier TFLite model (Gesture recognition model)'
    )

    use_static_image_mode_cmd = DeclareLaunchArgument(
        'use_static_image_mode',
        default_value='False',
        description='Wheter to treat the input images as single image or a video stream. ' \
                    'When False, it will try to detect hands in the first input images, '
                    'and upon a successful detection further localizes the hand landmarks.'
    )

    max_num_hands_cmd = DeclareLaunchArgument(
        'max_num_hands',
        default_value='1',
        description='Maximum number of hands to detect'
    )

    model_complexity_cmd = DeclareLaunchArgument(
        'model_complexity',
        default_value='1',
        choices=["0", "1"],
        description='Model complexity (0 or 1)'
    )

    debug_image_cmd = DeclareLaunchArgument(
        'debug_image',
        default_value='True',
        description='Whether to show the debug image window'
    )

    min_detection_confidence_cmd = DeclareLaunchArgument(
        'min_detection_confidence',
        default_value='0.7',
        description='Minimum detection confidence threshold'
    )

    min_tracking_confidence_cmd = DeclareLaunchArgument(
        'min_tracking_confidence',
        default_value='0.7',
        description='Minimum tracking confidence threshold'
    )

    input_image_topic_cmd = DeclareLaunchArgument(
        'input_image_topic',
        default_value='/image_raw',
        description='Topic to subscribe for input images'
    )

    image_reliability_cmd = DeclareLaunchArgument(
        "image_reliability",
        default_value="1",
        choices=["0", "1", "2"],
        description="Specific reliability QoS of the input image topic (0=system default, 1=Reliable, 2=Best Effort)",
    )


    # 3. Define the Node
    mediapipe_node = Node(
        package='mediapipe_ros',
        executable='mediapipe_node',
        name='mediapipe_node',
        output='screen',
        parameters=[{
            'keypoint_classifier_label': LaunchConfiguration('keypoint_classifier_label'),
            'keypoint_classifier_model': LaunchConfiguration('keypoint_classifier_model'),
            'use_static_image_mode': LaunchConfiguration('use_static_image_mode'),
            'debug_image': LaunchConfiguration('debug_image'),
            'min_detection_confidence': LaunchConfiguration('min_detection_confidence'),
            'min_tracking_confidence': LaunchConfiguration('min_tracking_confidence'),
            'image_reliability': LaunchConfiguration('image_reliability'),
        }],
        remappings=[
            ('image_raw', LaunchConfiguration('input_image_topic'))
        ]
    )

    # 4. Return Launch Description
    return LaunchDescription([
        keypoint_classifier_label_cmd,
        keypoint_classifier_model_cmd,
        use_static_image_mode_cmd,
        max_num_hands_cmd,
        model_complexity_cmd,
        debug_image_cmd,
        min_detection_confidence_cmd,
        min_tracking_confidence_cmd,
        input_image_topic_cmd,
        image_reliability_cmd,
        mediapipe_node
    ])