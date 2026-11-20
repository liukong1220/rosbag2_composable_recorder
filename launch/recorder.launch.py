import launch
from launch.actions import DeclareLaunchArgument as LaunchArg
from launch.actions import OpaqueFunction
from launch.substitutions import LaunchConfiguration as LaunchConfig
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from launch_ros.parameter_descriptions import ParameterValue


def launch_setup(context, *args, **kwargs):
    """Create composable recorder node."""
    bag_prefix = LaunchConfig("bag_prefix")
    storage_id = LaunchConfig("storage_id")
    record_all = ParameterValue(LaunchConfig("record_all"), value_type=bool)
    disable_discovery = ParameterValue(LaunchConfig("disable_discovery"), value_type=bool)
    start_recording_immediately = ParameterValue(
        LaunchConfig("start_recording_immediately"), value_type=bool
    )
    raw_topics = LaunchConfig("topics").perform(context).strip()
    topics = [topic.strip() for topic in raw_topics.split(",") if topic.strip()]

    container = ComposableNodeContainer(
        name="composable_recorder_container",
        namespace="",
        package="rclcpp_components",
        executable="component_container",
        composable_node_descriptions=[
            ComposableNode(
                package="rosbag2_composable_recorder",
                plugin="rosbag2_composable_recorder::ComposableRecorder",
                name="recorder",
                parameters=[
                    {
                        "topics": topics,
                        "storage_id": storage_id,
                        "record_all": record_all,
                        "disable_discovery": disable_discovery,
                        "serialization_format": "cdr",
                        "start_recording_immediately": start_recording_immediately,
                        "bag_prefix": bag_prefix,
                    }
                ],
                remappings=[],
                extra_arguments=[{"use_intra_process_comms": True}],
            )
        ],
        output="screen",
    )
    return [container]


def generate_launch_description():
    """Create composable recorder launch description."""
    return launch.LaunchDescription(
        [
            LaunchArg(
                "bag_prefix",
                default_value="rosbag_sentry_",
                description="Prefix for recorded rosbag2 directories.",
            ),
            LaunchArg(
                "storage_id",
                default_value="sqlite3",
                description="rosbag2 storage plugin id (e.g., sqlite3 or mcap).",
            ),
            LaunchArg(
                "topics",
                default_value="/serial/gimbal_joint_state,/livox/imu,/livox/lidar",
                description="Comma-separated list of topics to record when record_all is false.",
            ),
            LaunchArg(
                "record_all",
                default_value="false",
                description="Record all discovered topics when true.",
            ),
            LaunchArg(
                "disable_discovery",
                default_value="false",
                description="Disable dynamic topic discovery while recording.",
            ),
            LaunchArg(
                "start_recording_immediately",
                default_value="false",
                description="Start recording immediately on node startup.",
            ),
            OpaqueFunction(function=launch_setup),
        ]
    )
